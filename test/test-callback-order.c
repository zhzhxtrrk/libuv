/* Copyright Joyent, Inc. and other Node contributors. All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

/* This test is a port of test/simple/test-next-tick-ordering2.js */

#include "uv.h"
#include "task.h"

typedef void (*next_tick_cb)(uv_loop_t*);
static next_tick_cb tick_cb;

static uv_prepare_t prepare_tick_handle;
static uv_check_t check_tick_handle;
static uv_idle_t idle_tick_handle;
static uv_timer_t timer_handle;

static int timer_cb_called;
static int tick2_cb_called;


static void tick(uv_loop_t* loop) {
  next_tick_cb cb = tick_cb;
  tick_cb = NULL;
  if (cb) cb(loop);
}


static void prepare_tick(uv_prepare_t* handle, int status) {
  ASSERT(handle == &prepare_tick_handle);
  tick(handle->loop);
}


static void check_tick(uv_check_t* handle, int status) {
  ASSERT(handle == &check_tick_handle);
  tick(handle->loop);
}


static void idle_tick(uv_idle_t* handle, int status) {
  ASSERT(handle == &idle_tick_handle);
  uv_idle_stop(handle);
  tick(handle->loop);
}


static void next_tick(uv_loop_t* loop, next_tick_cb cb) {
  tick_cb = cb;
  uv_idle_start(&idle_tick_handle, idle_tick);
}


static void timer_cb(uv_timer_t* handle, int status) {
  ASSERT(timer_cb_called == 0);
  ASSERT(tick2_cb_called == 1);
  uv_timer_stop(handle);
  timer_cb_called++;
}


static void tick_2(uv_loop_t* loop) {
  ASSERT(timer_cb_called == 0);
  ASSERT(tick2_cb_called == 0);
  tick2_cb_called++;
}


static void tick_1(uv_loop_t* loop) {
  uv_timer_init(loop, &timer_handle);
  uv_timer_start(&timer_handle, timer_cb, 0, 0);
  next_tick(loop, tick_2);
}


TEST_IMPL(callback_order) {
  uv_loop_t* loop = uv_default_loop();

  uv_prepare_init(loop, &prepare_tick_handle);
  uv_check_init(loop, &check_tick_handle);
  uv_idle_init(loop, &idle_tick_handle);

  uv_prepare_start(&prepare_tick_handle, prepare_tick);
  uv_check_start(&check_tick_handle, check_tick);

  uv_unref((uv_handle_t*)&prepare_tick_handle);
  uv_unref((uv_handle_t*)&check_tick_handle);

  next_tick(loop, tick_1);

  ASSERT(timer_cb_called == 0);
  ASSERT(tick2_cb_called == 0);

  uv_run(loop);

  ASSERT(timer_cb_called == 1);
  ASSERT(tick2_cb_called == 1);

  return 0;
}

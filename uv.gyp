{
  'variables': {
    'visibility%': 'hidden',
    'target_arch%': 'ia32',
    'host_arch%': 'ia32',
    'library%': 'static_library',
    'msvs_multi_core_compile': '0',
    'gcc_version%': 'unknown',
    'clang%': 0,
  },

  'target_defaults': {
    'default_configuration': 'Debug',
    'conditions': [
      ['OS == "win"', {
        'msvs_cygwin_shell': 0, # prevent actions from trying to use cygwin
        'defines': [
          'WIN32',
          '_WIN32_WINNT=0x0600',
          # we don't really want VC++ warning us about
          # how dangerous C functions are...
          '_CRT_SECURE_NO_DEPRECATE',
          # ... or that C implementations shouldn't use
          # POSIX names
          '_CRT_NONSTDC_NO_DEPRECATE',
        ],
      }, {
        'defines': [
          '_XOPEN_SOURCE=500',
          '_LARGEFILE_SOURCE',
          '_FILE_OFFSET_BITS=64',
        ],
        'cflags': [
          '-pedantic',
          '-Wall',
          '-Wextra',
          '-Wno-unused-parameter'
        ],
        'link_settings': {
          'libraries': [ '-lm' ],
        },
      }],
      ['visibility=="hidden" and (clang==1 or gcc_version >= 40)', {
        'cflags': [ '-fvisibility=hidden' ],
      }],
      ['OS=="aix"', {
        'defines': [ '_ALL_SOURCE' ],
      }],
      ['OS=="linux"', {
        'defines': [ '_GNU_SOURCE' ],
      }],
      ['OS=="solaris"', {
        'defines': [ '__EXTENSIONS__' ],
      }],
      ['OS=="solaris"', {
        'cflags':  [ '-pthreads' ],
        'ldflags': [ '-pthreads' ],
      }, {
        'cflags':  [ '-pthread' ],
        'ldflags': [ '-pthread' ],
      }],
      ['target_arch != host_arch', {
        'target_conditions': [
          ['target_arch=="ia32"', {
            'cflags': [ '-m32' ],
            'ldflags': [ '-m32' ],
            'msvs_configuration_platform': 'x86',
          }],
          ['target_arch=="x64"', {
            'cflags': [ '-m64' ],
            'ldflags': [ '-m64' ],
            'msvs_configuration_platform': 'x64',
          }],
        ],
      }],
    ],
    'msvs_settings': {
      'VCCLCompilerTool': {
        'StringPooling': 'true', # pool string literals
        'DebugInformationFormat': 3, # Generate a PDB
        'WarningLevel': 3,
        'BufferSecurityCheck': 'true',
        'ExceptionHandling': 1, # /EHsc
        'SuppressStartupBanner': 'true',
        'WarnAsError': 'false',
        'AdditionalOptions': [
           '/MP', # compile across multiple CPUs
         ],
      },
      'VCLinkerTool': {
        'GenerateDebugInformation': 'true',
        'RandomizedBaseAddress': 2, # enable ASLR
        'DataExecutionPrevention': 2, # enable DEP
        'AllowIsolation': 'true',
        'SuppressStartupBanner': 'true',
        'target_conditions': [
          ['_type=="executable"', {
            'SubSystem': 1, # console executable
          }],
        ],
      },
    },
    'xcode_settings': {
      'ALWAYS_SEARCH_USER_PATHS': 'NO',
      'GCC_CW_ASM_SYNTAX': 'NO',                # No -fasm-blocks
      'GCC_DYNAMIC_NO_PIC': 'NO',               # No -mdynamic-no-pic
                                                # (Equivalent to -fPIC)
      'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',        # -fno-exceptions
      'GCC_ENABLE_CPP_RTTI': 'NO',              # -fno-rtti
      'GCC_ENABLE_PASCAL_STRINGS': 'NO',        # No -mpascal-strings
      # GCC_INLINES_ARE_PRIVATE_EXTERN maps to -fvisibility-inlines-hidden
      'GCC_INLINES_ARE_PRIVATE_EXTERN': 'YES',
      'GCC_SYMBOLS_PRIVATE_EXTERN': 'YES',      # -fvisibility=hidden
      'GCC_THREADSAFE_STATICS': 'NO',           # -fno-threadsafe-statics
      'GCC_WARN_ABOUT_MISSING_NEWLINE': 'YES',  # -Wnewline-eof
      'PREBINDING': 'NO',                       # No -Wl,-prebind
      'USE_HEADERMAP': 'NO',
      'OTHER_CFLAGS': [
        '-fno-strict-aliasing',
      ],
      'WARNING_CFLAGS': [
        '-Wall',
        '-Wendif-labels',
        '-W',
        '-Wno-unused-parameter',
      ],
    },
    'target_conditions': [
      ['_type=="static_library"', {
        'standalone_static_library': '1', # disable thin archive
      }, {
        'xcode_settings': {
          'OTHER_LDFLAGS': [ '-Wl,-search_paths_first' ]
        },
      }],
    ],
    'configurations': {
      'Debug': {
        'defines': [ 'DEBUG', '_DEBUG' ],
        'cflags': [ '-g', '-O0', '-fwrapv' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'target_conditions': [
              ['_type=="static_library"', {
                'RuntimeLibrary': 1, # static debug
              }, {
                'RuntimeLibrary': 3, # DLL debug
              }],
            ],
            'Optimization': 0, # /Od, no optimization
            'MinimalRebuild': 'false',
            'OmitFramePointers': 'false',
            'BasicRuntimeChecks': 3, # /RTC1
          },
          'VCLinkerTool': {
            'LinkIncremental': 2, # enable incremental linking
          },
        },
        'xcode_settings': {
          'GCC_OPTIMIZATION_LEVEL': '0',
        },
      },
      'Release': {
        'defines': [ 'NDEBUG' ],
        'cflags': [
          '-g',
          '-O3',
          '-fomit-frame-pointer',
          '-ffunction-sections',
          '-fdata-sections',
        ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'target_conditions': [
              ['_type=="static_library"', {
                'RuntimeLibrary': 0, # static release
              }, {
                'RuntimeLibrary': 2, # debug release
              }],
            ],
            'Optimization': 3, # /Ox, full optimization
            'FavorSizeOrSpeed': 1, # /Ot, favour speed over size
            'InlineFunctionExpansion': 2, # /Ob2, inline anything eligible
            'WholeProgramOptimization': 'true', # /GL, whole program optimization, needed for LTCG
            'OmitFramePointers': 'true',
            'EnableFunctionLevelLinking': 'true',
            'EnableIntrinsicFunctions': 'true',
          },
          'VCLibrarianTool': {
            'AdditionalOptions': [
              '/LTCG', # link time code generation
            ],
          },
          'VCLinkerTool': {
            'LinkTimeCodeGeneration': 1, # link-time code generation
            'OptimizeReferences': 2, # /OPT:REF
            'EnableCOMDATFolding': 2, # /OPT:ICF
            'LinkIncremental': 1, # disable incremental linking
          },
        },
      }
    },
  },

  'targets': [
    {
      'target_name': 'libuv',
      'type': '<(library)',
      'include_dirs': [
        'include',
        'include/uv-private',
        'src/',
      ],
      'direct_dependent_settings': {
        'include_dirs': [ 'include' ],
        'conditions': [
          ['OS != "win"', {
            'defines': [
              '_LARGEFILE_SOURCE',
              '_FILE_OFFSET_BITS=64',
              '_POSIX_C_SOURCE=200112',
            ],
          }],
          ['OS == "mac"', {
            'defines': [
              '_DARWIN_USE_64_BIT_INODE=1',
              '_DARWIN_C_SOURCE',  # _POSIX_C_SOURCE hides SysV definitions.
            ],
          }],
        ],
      },
      'sources': [
        'common.gypi',
        'include/uv.h',
        'include/uv-private/ngx-queue.h',
        'include/uv-private/tree.h',
        'src/fs-poll.c',
        'src/inet.c',
        'src/uv-common.c',
        'src/uv-common.h',
      ],
      'conditions': [
        [ 'OS=="win"', {
          'sources': [
            'include/uv-private/uv-win.h',
            'src/win/async.c',
            'src/win/atomicops-inl.h',
            'src/win/core.c',
            'src/win/dl.c',
            'src/win/error.c',
            'src/win/fs.c',
            'src/win/fs-event.c',
            'src/win/getaddrinfo.c',
            'src/win/handle.c',
            'src/win/handle-inl.h',
            'src/win/internal.h',
            'src/win/loop-watcher.c',
            'src/win/pipe.c',
            'src/win/thread.c',
            'src/win/poll.c',
            'src/win/process.c',
            'src/win/process-stdio.c',
            'src/win/req.c',
            'src/win/req-inl.h',
            'src/win/signal.c',
            'src/win/stream.c',
            'src/win/stream-inl.h',
            'src/win/tcp.c',
            'src/win/tty.c',
            'src/win/threadpool.c',
            'src/win/timer.c',
            'src/win/udp.c',
            'src/win/util.c',
            'src/win/winapi.c',
            'src/win/winapi.h',
            'src/win/winsock.c',
            'src/win/winsock.h',
          ],
          'link_settings': {
            'libraries': [
              '-lws2_32.lib',
              '-lpsapi.lib',
              '-liphlpapi.lib'
            ],
          },
        }, {
          'cflags': [ '-std=gnu89' ],
          'sources': [
            'include/uv-private/uv-unix.h',
            'include/uv-private/uv-linux.h',
            'include/uv-private/uv-sunos.h',
            'include/uv-private/uv-darwin.h',
            'include/uv-private/uv-bsd.h',
            'src/unix/async.c',
            'src/unix/core.c',
            'src/unix/dl.c',
            'src/unix/error.c',
            'src/unix/fs.c',
            'src/unix/getaddrinfo.c',
            'src/unix/internal.h',
            'src/unix/loop.c',
            'src/unix/loop-watcher.c',
            'src/unix/pipe.c',
            'src/unix/poll.c',
            'src/unix/process.c',
            'src/unix/signal.c',
            'src/unix/stream.c',
            'src/unix/tcp.c',
            'src/unix/thread.c',
            'src/unix/threadpool.c',
            'src/unix/timer.c',
            'src/unix/tty.c',
            'src/unix/udp.c',
          ],
          'conditions': [
            ['_type=="shared_library"', {
              'cflags': [ '-fPIC' ],
            }],
          ],
        }],
        [ 'OS=="mac"', {
          'sources': [ 'src/unix/darwin.c', 'src/unix/fsevents.c' ],
          'link_settings': {
            'libraries': [
              '$(SDKROOT)/System/Library/Frameworks/CoreServices.framework',
            ],
          },
          'defines': [
            '_DARWIN_USE_64_BIT_INODE=1',
          ]
        }],
        [ 'OS=="linux"', {
          'sources': [
            'src/unix/linux/linux-core.c',
            'src/unix/linux/inotify.c',
            'src/unix/linux/syscalls.c',
            'src/unix/linux/syscalls.h',
          ],
          'link_settings': {
            'libraries': [ '-ldl', '-lrt' ],
          },
        }],
        [ 'OS=="solaris"', {
          'sources': [ 'src/unix/sunos.c' ],
          'link_settings': {
            'libraries': [
              '-lkstat',
              '-lnsl',
              '-lsendfile',
              '-lsocket',
            ],
          },
        }],
        [ 'OS=="aix"', {
          'include_dirs': [ 'src/ares/config_aix' ],
          'sources': [ 'src/unix/aix.c' ],
          'defines': [ '_ALL_SOURCE' ],
          'link_settings': {
            'libraries': [
              '-lperfstat',
            ],
          },
        }],
        [ 'OS=="freebsd" or OS=="dragonflybsd"', {
          'sources': [ 'src/unix/freebsd.c' ],
          'link_settings': {
            'libraries': [
              '-lkvm',
            ],
          },
        }],
        [ 'OS=="openbsd"', {
          'sources': [ 'src/unix/openbsd.c' ],
        }],
        [ 'OS=="netbsd"', {
          'sources': [ 'src/unix/netbsd.c' ],
          'link_settings': {
            'libraries': [
              '-lkvm',
            ],
          },
        }],
        [ 'OS in "mac freebsd dragonflybsd openbsd netbsd".split()', {
          'sources': [ 'src/unix/kqueue.c' ],
        }],
        ['_type=="shared_library"', {
          'defines': [ 'BUILDING_UV_SHARED=1' ]
        }]
      ]
    },

    {
      'target_name': 'run-tests',
      'type': 'executable',
      'dependencies': [ 'libuv' ],
      'sources': [
        'test/blackhole-server.c',
        'test/echo-server.c',
        'test/run-tests.c',
        'test/runner.c',
        'test/runner.h',
        'test/test-get-loadavg.c',
        'test/task.h',
        'test/test-util.c',
        'test/test-active.c',
        'test/test-async.c',
        'test/test-callback-stack.c',
        'test/test-callback-order.c',
        'test/test-connection-fail.c',
        'test/test-cwd-and-chdir.c',
        'test/test-delayed-accept.c',
        'test/test-error.c',
        'test/test-embed.c',
        'test/test-fail-always.c',
        'test/test-fs.c',
        'test/test-fs-event.c',
        'test/test-get-currentexe.c',
        'test/test-get-memory.c',
        'test/test-getaddrinfo.c',
        'test/test-getsockname.c',
        'test/test-hrtime.c',
        'test/test-idle.c',
        'test/test-ipc.c',
        'test/test-ipc-send-recv.c',
        'test/test-list.h',
        'test/test-loop-handles.c',
        'test/test-walk-handles.c',
        'test/test-multiple-listen.c',
        'test/test-pass-always.c',
        'test/test-ping-pong.c',
        'test/test-pipe-bind-error.c',
        'test/test-pipe-connect-error.c',
        'test/test-platform-output.c',
        'test/test-poll.c',
        'test/test-poll-close.c',
        'test/test-process-title.c',
        'test/test-ref.c',
        'test/test-run-nowait.c',
        'test/test-run-once.c',
        'test/test-semaphore.c',
        'test/test-shutdown-close.c',
        'test/test-shutdown-eof.c',
        'test/test-signal.c',
        'test/test-signal-multiple-loops.c',
        'test/test-spawn.c',
        'test/test-fs-poll.c',
        'test/test-stdio-over-pipes.c',
        'test/test-tcp-bind-error.c',
        'test/test-tcp-bind6-error.c',
        'test/test-tcp-close.c',
        'test/test-tcp-close-while-connecting.c',
        'test/test-tcp-connect-error-after-write.c',
        'test/test-tcp-shutdown-after-write.c',
        'test/test-tcp-flags.c',
        'test/test-tcp-connect-error.c',
        'test/test-tcp-connect-timeout.c',
        'test/test-tcp-connect6-error.c',
        'test/test-tcp-open.c',
        'test/test-tcp-write-error.c',
        'test/test-tcp-write-to-half-open-connection.c',
        'test/test-tcp-writealot.c',
        'test/test-tcp-unexpected-read.c',
        'test/test-tcp-read-stop.c',
        'test/test-threadpool.c',
        'test/test-threadpool-cancel.c',
        'test/test-mutexes.c',
        'test/test-thread.c',
        'test/test-barrier.c',
        'test/test-condvar.c',
        'test/test-condvar-consumer-producer.c',
        'test/test-timer-again.c',
        'test/test-timer.c',
        'test/test-tty.c',
        'test/test-udp-dgram-too-big.c',
        'test/test-udp-ipv6.c',
        'test/test-udp-open.c',
        'test/test-udp-options.c',
        'test/test-udp-send-and-recv.c',
        'test/test-udp-multicast-join.c',
        'test/test-dlerror.c',
        'test/test-udp-multicast-ttl.c',
      ],
      'conditions': [
        ['OS=="win"', {
          'sources': [
            'test/runner-win.c',
            'test/runner-win.h'
          ],
          'libraries': [ 'ws2_32.lib' ]
        }, {
          'sources': [
            'test/runner-unix.c',
            'test/runner-unix.h',
          ],
        }],
      ],
      'msvs-settings': {
        'VCLinkerTool': {
          'SubSystem': 1, # /subsystem:console
        },
      },
    },

    {
      'target_name': 'run-benchmarks',
      'type': 'executable',
      'dependencies': [ 'libuv' ],
      'sources': [
        'test/benchmark-async.c',
        'test/benchmark-async-pummel.c',
        'test/benchmark-fs-stat.c',
        'test/benchmark-getaddrinfo.c',
        'test/benchmark-list.h',
        'test/benchmark-loop-count.c',
        'test/benchmark-million-async.c',
        'test/benchmark-million-timers.c',
        'test/benchmark-multi-accept.c',
        'test/benchmark-ping-pongs.c',
        'test/benchmark-pound.c',
        'test/benchmark-pump.c',
        'test/benchmark-sizes.c',
        'test/benchmark-spawn.c',
        'test/benchmark-thread.c',
        'test/benchmark-tcp-write-batch.c',
        'test/benchmark-udp-pummel.c',
        'test/dns-server.c',
        'test/echo-server.c',
        'test/blackhole-server.c',
        'test/run-benchmarks.c',
        'test/runner.c',
        'test/runner.h',
        'test/task.h',
      ],
      'conditions': [
        [ 'OS=="win"', {
          'sources': [
            'test/runner-win.c',
            'test/runner-win.h',
          ],
          'libraries': [ 'ws2_32.lib' ]
        }, {
          'sources': [
            'test/runner-unix.c',
            'test/runner-unix.h',
          ]
        }],
      ],
      'msvs-settings': {
        'VCLinkerTool': {
          'SubSystem': 1, # /subsystem:console
        },
      },
    }
  ]
}



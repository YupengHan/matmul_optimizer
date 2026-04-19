cmake_minimum_required(VERSION 3.22)

project(matmul_optimizer LANGUAGES CXX CUDA)

if(NOT CMAKE_CUDA_ARCHITECTURES)
  set(CMAKE_CUDA_ARCHITECTURES 86)
endif()

include(FetchContent)

find_package(CUDAToolkit REQUIRED)

set(RUNNER_SOURCES
  src/runner/main.cpp
)

set(KERNEL_SOURCES
  src/kernels/bf16_gemm_v1.cu
)

function(configure_runner_target target_name)
  target_include_directories(${target_name} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
  )

  target_compile_features(${target_name} PRIVATE cxx_std_17)

  target_compile_options(${target_name} PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-lineinfo>
  )

  set_target_properties(${target_name} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CUDA_STANDARD 17
    CUDA_STANDARD_REQUIRED ON
    CUDA_SEPARABLE_COMPILATION ON
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
  )

  target_link_libraries(${target_name} PRIVATE CUDA::cudart)
endfunction()

add_executable(custom_runner
  ${RUNNER_SOURCES}
  ${KERNEL_SOURCES}
)

configure_runner_target(custom_runner)

option(ENABLE_CUTLASS_RUNNER "Build the CUTLASS baseline runner target" OFF)
set(CUTLASS_ROOT "" CACHE PATH "Path to a local CUTLASS checkout")
set(CUTLASS_URL "https://codeload.github.com/NVIDIA/cutlass/tar.gz/refs/tags/v3.5.1")
set(CUTLASS_URL_HASH "SHA256=20b7247cda2d257cbf8ba59ba3ca40a9211c4da61a9c9913e32b33a2c5883a36")

if(ENABLE_CUTLASS_RUNNER)
  if(CUTLASS_ROOT)
    if(NOT EXISTS "${CUTLASS_ROOT}/include/cutlass/cutlass.h")
      message(FATAL_ERROR "CUTLASS_ROOT does not look like a valid CUTLASS checkout: ${CUTLASS_ROOT}")
    endif()
    set(CUTLASS_SOURCE_DIR "${CUTLASS_ROOT}")
  else()
    FetchContent_Declare(
      cutlass_src
      URL ${CUTLASS_URL}
      URL_HASH ${CUTLASS_URL_HASH}
    )
    FetchContent_GetProperties(cutlass_src)
    if(NOT cutlass_src_POPULATED)
      FetchContent_Populate(cutlass_src)
    endif()
    set(CUTLASS_SOURCE_DIR "${cutlass_src_SOURCE_DIR}")
  endif()

  add_executable(cutlass_runner
    src/runner/cutlass_main.cu
  )

  configure_runner_target(cutlass_runner)

  target_include_directories(cutlass_runner PRIVATE
    ${CUTLASS_SOURCE_DIR}/include
  )

  target_compile_options(cutlass_runner PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:--expt-relaxed-constexpr>
    $<$<COMPILE_LANGUAGE:CUDA>:--extended-lambda>
  )
endif()

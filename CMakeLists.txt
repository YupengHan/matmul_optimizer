cmake_minimum_required(VERSION 3.22)

project(matmul_optimizer LANGUAGES CXX CUDA)

if(NOT CMAKE_CUDA_ARCHITECTURES)
  set(CMAKE_CUDA_ARCHITECTURES 86)
endif()

find_package(CUDAToolkit REQUIRED)

set(RUNNER_SOURCES
  src/runner/main.cpp
)

set(KERNEL_SOURCES
  src/kernels/bf16_gemm_v1.cu
)

add_executable(custom_runner
  ${RUNNER_SOURCES}
  ${KERNEL_SOURCES}
)

target_include_directories(custom_runner PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(custom_runner PRIVATE cxx_std_17)

set_target_properties(custom_runner PROPERTIES
  CXX_STANDARD 17
  CXX_STANDARD_REQUIRED ON
  CUDA_STANDARD 17
  CUDA_STANDARD_REQUIRED ON
  CUDA_SEPARABLE_COMPILATION ON
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

target_link_libraries(custom_runner PRIVATE CUDA::cudart)

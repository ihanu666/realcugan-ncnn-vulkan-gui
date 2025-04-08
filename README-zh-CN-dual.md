# Real-CUGAN ncnn Vulkan

:exclamation: :exclamation: :exclamation: 该软件处于早期开发阶段，它可能会咬你的猫

![CI](https://github.com/nihui/realcugan-ncnn-vulkan/workflows/CI/badge.svg)
![download](https://img.shields.io/github/downloads/nihui/realcugan-ncnn-vulkan/total.svg)

ncnn 实现的 Real-CUGAN 转换器。在 Intel / AMD / Nvidia / Apple-Silicon 上使用 Vulkan API 运行速度快。

realcugan-ncnn-vulkan 使用 [ncnn 项目](https://github.com/Tencent/ncnn)作为通用神经网络推理框架。

## [下载](https://github.com/nihui/realcugan-ncnn-vulkan/releases)

下载适用于 Intel/AMD/Nvidia/Apple-Silicon GPU 的 Windows/Linux/MacOS 可执行文件

**https://github.com/nihui/realcugan-ncnn-vulkan/releases**

该软件包包含所有必需的二进制文件和模型。它是便携式的，因此不需要 CUDA 或 PyTorch 运行时环境 :)

## 关于 Real-CUGAN

Real-CUGAN（用于动漫图像超分辨率的真实级联 U-Nets）

https://github.com/bilibili/ailab/tree/main/Real-CUGAN

## 用途

### 示例命令

```
realcugan-ncnn-vulkan.exe -i input.jpg -o output.png
```

### 完整用法

```console
Usage: realcugan-ncnn-vulkan -i infile -o outfile [options]...

  -h                   show this help
  -v                   verbose output
  -i input-path        input image path (jpg/png/webp) or directory
  -o output-path       output image path (jpg/png/webp) or directory
  -n noise-level       denoise level (-1/0/1/2/3, default=-1)
  -s scale             upscale ratio (1/2/3/4, default=2)
  -t tile-size         tile size (>=32/0=auto, default=0) can be 0,0,0 for multi-gpu
  -c syncgap-mode      sync gap mode (0/1/2/3, default=3)
  -m model-path        realcugan model path (default=models-se)
  -g gpu-id            gpu device to use (-1=cpu, default=auto) can be 0,1,2 for multi-gpu
  -j load:proc:save    thread count for load/proc/save (default=1:2:2) can be 1:2,2,2:2 for multi-gpu
  -x                   enable tta mode
  -f format            output image format (jpg/png/webp, default=ext/png)
```

- `input-path` and `output-path` accept either file path or directory path
- `noise-level` = noise level, large value means strong denoise effect, -1 = no effect
- `scale` = scale level, 1 = no scaling, 2 = upscale 2x
- `tile-size` = tile size, use smaller value to reduce GPU memory usage, default selects automatically
- `syncgap-mode` = sync gap mode, 0 = no sync, 1 = accurate sync, 2 = rough sync, 3 = very rough sync
- `load:proc:save` = thread count for the three stages (image decoding + realcugan upscaling + image encoding), using larger values may increase GPU usage and consume more GPU memory. You can tune this configuration with "4:4:4" for many small-size images, and "2:2:2" for large-size images. The default setting usually works fine for most situations. If you find that your GPU is hungry, try increasing thread count to achieve faster processing.
- `format` = the format of the image to be output, png is better supported, however webp generally yields smaller file sizes, both are losslessly encoded

If you encounter a crash or error, try upgrading your GPU driver:

- Intel: https://downloadcenter.intel.com/product/80939/Graphics-Drivers
- AMD: https://www.amd.com/en/support
- NVIDIA: https://www.nvidia.com/Download/index.aspx

## Build from Source

1. Download and setup the Vulkan SDK from https://vulkan.lunarg.com/
  - For Linux distributions, you can either get the essential build requirements from package manager
```shell
dnf install vulkan-headers vulkan-loader-devel
```
```shell
apt-get install libvulkan-dev
```
```shell
pacman -S vulkan-headers vulkan-icd-loader
```

2. Clone this project with all submodules

```shell
git clone https://github.com/nihui/realcugan-ncnn-vulkan.git
cd realcugan-ncnn-vulkan
git submodule update --init --recursive
```

3. Build with CMake
  - You can pass -DUSE_STATIC_MOLTENVK=ON option to avoid linking the vulkan loader library on MacOS

```shell
mkdir build
cd build
cmake ../src
cmake --build . -j 4
```

## Sample Images

### Original Image

![origin](images/0.jpg)

### Upscale 2x with ImageMagick

```shell
convert origin.jpg -resize 200% output.png
```

![browser](images/1.png)

### Upscale 2x with ImageMagick Lanczo4 Filter

```shell
convert origin.jpg -filter Lanczos -resize 200% output.png
```

![browser](images/4.png)

### Upscale 2x with Real-CUGAN

```shell
realcugan-ncnn-vulkan.exe -i origin.jpg -o output.png -s 2 -n 1 -x
```

![realcugan](images/2.png)

## Original Real-CUGAN Project

- https://github.com/bilibili/ailab/tree/main/Real-CUGAN

## Other Open-Source Code Used

- https://github.com/Tencent/ncnn for fast neural network inference on ALL PLATFORMS
- https://github.com/webmproject/libwebp for encoding and decoding Webp images on ALL PLATFORMS
- https://github.com/nothings/stb for decoding and encoding image on Linux / MacOS
- https://github.com/tronkko/dirent for listing files in directory on Windows

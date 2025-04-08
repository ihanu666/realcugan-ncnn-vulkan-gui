# Real-CUGAN ncnn Vulkan

:exclamation: :exclamation: :exclamation: This software is in the early development stage, it may bite your cat
:exclamation: :exclamation: :exclamation: 该软件处于早期开发阶段，它可能会咬你的猫

![CI](https://github.com/nihui/realcugan-ncnn-vulkan/workflows/CI/badge.svg) ![download](https://img.shields.io/github/downloads/nihui/realcugan-ncnn-vulkan/total.svg)

ncnn implementation of Real-CUGAN converter. Runs fast on Intel / AMD / Nvidia / Apple-Silicon with Vulkan API.
ncnn 实现的 Real-CUGAN 转换器。在 Intel / AMD / Nvidia / Apple-Silicon 上使用 Vulkan API 运行速度快。

realcugan-ncnn-vulkan uses [ncnn project](https://github.com/Tencent/ncnn) as the universal neural network inference framework.
realcugan-ncnn-vulkan 使用 ncnn 项目作为通用神经网络推理框架。

## [Download
下载](https://github.com/nihui/realcugan-ncnn-vulkan/releases)

Download Windows/Linux/MacOS Executable for Intel/AMD/Nvidia/Apple-Silicon GPU
下载适用于 Intel/AMD/Nvidia/Apple-Silicon GPU 的 Windows/Linux/MacOS 可执行文件

**[https://github.com/nihui/realcugan-ncnn-vulkan/releases](https://github.com/nihui/realcugan-ncnn-vulkan/releases)**

This package includes all the binaries and models required. It is portable, so no CUDA or PyTorch runtime environment is needed :)
该软件包包含所有必需的二进制文件和模型。它是便携式的，因此不需要 CUDA 或 PyTorch 运行时环境 :)

## About Real-CUGAN
关于 Real-CUGAN

Real-CUGAN (Real Cascade U-Nets for Anime Image Super Resolution)
Real-CUGAN（用于动漫图像超分辨率的真实级联 U-Nets）

[https://github.com/bilibili/ailab/tree/main/Real-CUGAN](https://github.com/bilibili/ailab/tree/main/Real-CUGAN)

## Usages
用途
### Example Command
示例命令

realcugan-ncnn-vulkan.exe -i input.jpg -o output.png


### Full Usages
完整用法

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


*   `input-path` and `output-path` accept either file path or directory path
`input-path` 和 `output-path` 接受文件路径或目录路径
*   `noise-level` = noise level, large value means strong denoise effect, -1 = no effect
`noise-level` = 噪声级别，数值越大表示去噪效果越强，-1 = 无效果
*   `scale` = scale level, 1 = no scaling, 2 = upscale 2x
`scale` = 缩放级别，1 = 不缩放，2 = 放大 2 倍
*   `tile-size` = tile size, use smaller value to reduce GPU memory usage, default selects automatically
`tile-size` = 瓦片大小，使用较小的值以减少 GPU 内存使用量，默认自动选择
*   `syncgap-mode` = sync gap mode, 0 = no sync, 1 = accurate sync, 2 = rough sync, 3 = very rough sync
`syncgap-mode` = 同步间隙模式，0 = 无同步，1 = 精确同步，2 = 粗略同步，3 = 非常粗略同步
*   `load:proc:save` = thread count for the three stages (image decoding + realcugan upscaling + image encoding), using larger values may increase GPU usage and consume more GPU memory. You can tune this configuration with "4:4:4" for many small-size images, and "2:2:2" for large-size images. The default setting usually works fine for most situations. If you find that your GPU is hungry, try increasing thread count to achieve faster processing.
`load:proc:save` = 三个阶段的线程数（图像解码 + realcugan 放大 + 图像编码），使用较大的值可能会增加 GPU 使用率并消耗更多 GPU 内存。对于许多小尺寸图像，可以使用 "4:4:4" 来调整此配置，对于大尺寸图像，可以使用 "2:2:2"。默认设置在大多数情况下通常都能正常工作。如果发现 GPU 资源不足，可以尝试增加线程数以实现更快的处理速度。
*   `format` = the format of the image to be output, png is better supported, however webp generally yields smaller file sizes, both are losslessly encoded
`format` = 要输出的图像格式，png 支持较好，但 webp 通常生成的文件更小，两者都是无损编码

If you encounter a crash or error, try upgrading your GPU driver:
如果遇到崩溃或错误，请尝试升级您的 GPU 驱动程序：

*   Intel: [https://downloadcenter.intel.com/product/80939/Graphics-Drivers](https://downloadcenter.intel.com/product/80939/Graphics-Drivers)
*   AMD: [https://www.amd.com/en/support](https://www.amd.com/en/support)
*   NVIDIA: [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)

## Build from Source
从源代码构建

1. Download and setup the Vulkan SDK from [https://vulkan.lunarg.com/](https://vulkan.lunarg.com/)
从 https://vulkan.lunarg.com/ 下载并安装 Vulkan SDK

*   For Linux distributions, you can either get the essential build requirements from package manager
对于 Linux 发行版，您可以从包管理器中获取基本的构建要求

dnf install vulkan-headers vulkan-loader-devel


apt-get install libvulkan-dev


pacman -S vulkan-headers vulkan-icd-loader


1. Clone this project with all submodules
克隆此项目及其所有子模块

git clone https://github.com/nihui/realcugan-ncnn-vulkan.git
cd realcugan-ncnn-vulkan
git submodule update --init --recursive


1. Build with CMake
使用 CMake 构建

*   You can pass -DUSE\_STATIC\_MOLTENVK=ON option to avoid linking the vulkan loader library on MacOS
您可以通过传递 \`-DUSE\_STATIC\_MOLTENVK=ON\` 选项来避免在 MacOS 上链接 vulkan loader 库

mkdir build
cd build
cmake ../src
cmake --build . -j 4


## Sample Images
示例图片
### Original Image
原始图像

![origin](images/0.jpg)

### Upscale 2x with ImageMagick
使用 ImageMagick 进行 2 倍放大

convert origin.jpg -resize 200% output.png


![browser](images/1.png)

### Upscale 2x with ImageMagick Lanczo4 Filter
使用 ImageMagick 的 Lanczo4 滤镜进行 2 倍放大

convert origin.jpg -filter Lanczos -resize 200% output.png


![browser](images/4.png)

### Upscale 2x with Real-CUGAN
使用 Real-CUGAN 进行 2 倍放大

realcugan-ncnn-vulkan.exe -i origin.jpg -o output.png -s 2 -n 1 -x


![realcugan](images/2.png)

## Original Real-CUGAN Project
Original Real-CUGAN 项目

*   [https://github.com/bilibili/ailab/tree/main/Real-CUGAN](https://github.com/bilibili/ailab/tree/main/Real-CUGAN)

## Other Open-Source Code Used
其他使用的开源代码

*   [https://github.com/Tencent/ncnn](https://github.com/Tencent/ncnn) for fast neural network inference on ALL PLATFORMS
https://github.com/Tencent/ncnn 用于在所有平台上进行快速神经网络推理
*   [https://github.com/webmproject/libwebp](https://github.com/webmproject/libwebp) for encoding and decoding Webp images on ALL PLATFORMS
https://github.com/webmproject/libwebp 用于在所有平台上编码和解码 Webp 图像
*   [https://github.com/nothings/stb](https://github.com/nothings/stb) for decoding and encoding image on Linux / MacOS
https://github.com/nothings/stb 用于在 Linux / MacOS 上解码和编码图像
*   [https://github.com/tronkko/dirent](https://github.com/tronkko/dirent) for listing files in directory on Windows
https://github.com/tronkko/dirent 用于在 Windows 上列出目录中的文件


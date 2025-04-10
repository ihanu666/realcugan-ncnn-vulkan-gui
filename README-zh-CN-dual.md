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
用法：realcugan-ncnn-vulkan -i 输入文件 -o 输出文件 [选项]...

  -h                   显示此帮助信息
  -v                   显示详细输出
  -i input-path        输入图像路径（jpg/png/webp）或目录
  -o output-path       输出图像路径（jpg/png/webp）或目录
  -n noise-level       降噪等级（-1/0/1/2/3，默认=-1）
  -s scale             放大倍数 (1/2/3/4, 默认=2)
  -t tile-size         分块大小（>=32/0=自动，默认=0），有多个GPU可以设为0,0,0
  -c syncgap-mode      同步间隔模式 (0/1/2/3, 默认=3)
  -m model-path        模型路径（默认=models-se）
  -g gpu-id            使用的GPU编号（-1=CPU，默认=自动），有多个GPU可以设为0,1,2
  -j load:proc:save    加载/处理/保存的线程数（默认=1:2:2），有多个GPU可以设为1:2,2,2:2
  -x                   启用tta模式
  -f format            输出图像格式（jpg/png/webp，默认=ext/png）
```

- `input-path` 和 `output-path` 接受文件路径或目录路径
- `noise-level` = 降噪等级，数值越大表示去噪效果越强，-1 = 无效果
- `scale` = 放大倍数, 1 = 不放大, 2 = 放大2倍
- `tile-size` = 分块大小，使用较小的值以减少GPU内存使用，默认自动选择
- `syncgap-mode` = 同步间隔模式，0 = 无同步，1 = 精确同步，2 = 粗略同步，3 = 非常粗略的同步
- `load:proc:save` = 三个阶段的线程数（图像解码 + realcugan放大 + 图像编码），使用较大的值可能会增加GPU使用率并消耗更多GPU内存。对于许多小尺寸图像，可以使用"4:4:4"来调整此配置，对于大尺寸图像，可以使用"2:2:2"。默认设置在大多数情况下都能正常工作。如果发现GPU资源不足，可以尝试增加线程数以加快处理速度。
- `format` = 要输出的图像格式，png支持较好，但webp通常生成的文件更小，两者都是无损编码

如果遇到崩溃或错误，请尝试更新您的GPU驱动：

- Intel: https://downloadcenter.intel.com/product/80939/Graphics-Drivers
- AMD: https://www.amd.com/en/support
- NVIDIA: https://www.nvidia.com/Download/index.aspx

## 从源代码构建

1. 从https://vulkan.lunarg.com/下载并安装Vulkan SDK
  - 对于Linux发行版，你可以从包管理器中获取基本的构建要求
```shell
dnf install vulkan-headers vulkan-loader-devel
```
```shell
apt-get install libvulkan-dev
```
```shell
pacman -S vulkan-headers vulkan-icd-loader
```

2. 克隆此项目及其所有子模块

```shell
git clone https://github.com/nihui/realcugan-ncnn-vulkan.git
cd realcugan-ncnn-vulkan
git submodule update --init --recursive
```

3. 使用 CMake 构建
  - 你可以在MacOS上传递-DUSE_STATIC_MOLTENVK=ON选项来避免链接vulkan加载器库
```shell
mkdir build
cd build
cmake ../src
cmake --build . -j 4
```

## 示例图片

### 原始图像

![origin](images/0.jpg)

### 使用ImageMagick进行2倍放大

```shell
convert origin.jpg -resize 200% output.png
```

![browser](images/1.png)

### 使用ImageMagick的Lanczo4滤镜进行2倍放大

```shell
convert origin.jpg -filter Lanczos -resize 200% output.png
```

![browser](images/4.png)

### 使用Real-CUGAN进行2倍放大

```shell
realcugan-ncnn-vulkan.exe -i origin.jpg -o output.png -s 2 -n 1 -x
```

![realcugan](images/2.png)

## 原始Real-CUGAN项目

- https://github.com/bilibili/ailab/tree/main/Real-CUGAN

## 使用的其他开源代码

- https://github.com/Tencent/ncnn for fast neural network inference on ALL PLATFORMS
- https://github.com/webmproject/libwebp for encoding and decoding Webp images on ALL PLATFORMS
- https://github.com/nothings/stb for decoding and encoding image on Linux / MacOS
- https://github.com/tronkko/dirent for listing files in directory on Windows

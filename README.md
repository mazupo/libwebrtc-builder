# libwebrtc-builder

[![libwebrtc](https://img.shields.io/github/v/release/mazupo/libwebrtc-builder?label=libwebrtc%20branch)](https://github.com/mazupo/libwebrtc-builder/releases)

This repository provides an automated way to build the native WebRTC library for the ARM64 platform using GitHub Actions. The primary purpose of this build is to support the [pi-webrtc](https://github.com/mazupo/pi-webrtc) project.

## Release Artifacts

Each successful build produces a release containing the following artifact:

- **libwebrtc-arm64.tar.gz**
  - WebRTC header files (`include/*.h`)
  - WebRTC static library (`lib/libwebrtc.a`)

You can download the latest release from the [Releases](https://github.com/mazupo/libwebrtc-builder/releases) page.

## Usage

To use the compiled WebRTC library in your ARM64 project, download the `libwebrtc-arm64.tar.gz` file and extract it:

```sh
tar -xzf libwebrtc-arm64.tar.gz -C /your/destination/path
```

Include the extracted headers and link the static library in your project.

## Build Process

The build process leverages a custom GitHub Actions workflow to compile WebRTC from the official source: [WebRTC Source](https://webrtc.googlesource.com/src).

### Build Configuration

The WebRTC build is configured with the following parameters:

```sh
gn gen out/Release --args="
    target_os=\"linux\"
    target_cpu=\"arm64\"
    is_debug=false
    rtc_include_tests=false
    rtc_use_x11=false
    rtc_use_h264=true
    rtc_use_pipewire=false
    use_rtti=true
    use_glib=false
    use_custom_libcxx=false
    rtc_build_tools=false
    rtc_build_examples=false
    is_component_build=false
    is_component_ffmpeg=true
    ffmpeg_branding=\"Chrome\"
    proprietary_codecs=true
    clang_use_chrome_plugins=false
"
```

## Version Management

WebRTC versions are managed based on the releases listed on [Chromium Dash](https://chromiumdash.appspot.com/branches). When a new version is released, a corresponding tag is created in this repository.

Once the tag is pushed to GitHub, it triggers the GitHub Actions workflow to start the build process. After the build completes, an automatic release is generated containing the compiled WebRTC artifacts.

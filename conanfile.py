from conans import ConanFile, CMake
from os import environ


class SECP256K1Conan(ConanFile):
    name = "SECP256K1"
    version = "0.2.0"
    license = "MIT"
    author = ""
    url = "https://github.com/Gigamonkey-BSV/secp256k1"
    description = "Optimized C library for EC operations on curve secp256k1 "
    topics = ("Ecliptical Curve", "secp256k1")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "*"
    requires = "autoconf/2.71", "automake/1.16.3", "libtool/2.4.6"

    def set_version(self):
        if "CIRCLE_TAG" in environ:
            self.version = environ.get("CIRCLE_TAG")[1:]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        self.run("./autogen.sh")
        self.run("./configure --disable-debug --disable-dependency-tracking --disable-silent-rules --prefix=$(pwd)")
        self.run("make")

    def package(self):
        self.copy("*.h", dst="include", src="include")

        if self.options.shared == False:
            self.copy("*.a", dst="lib", keep_path=False)
            self.copy("*.lib", dst="lib", keep_path=False)
        else:
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["secp256k1"]

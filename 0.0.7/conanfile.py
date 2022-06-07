from conans import ConanFile, CMake, tools
import os

class EmeraldConan(ConanFile):
    name = "emerald"
    version = "0.0.7"
    license = "Apache 2.0"
    url = "https://github.com/blackencino/emerald"
    description = "Emerald Simulation Libraries"
    topics = ("conan", "simulation", "emerald", "sph", "fluids", "cfd", "vfx")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False],
        "build_guis": [True, False]
        }
    default_options = {
        "shared": False, 
        "fPIC": True,
        "build_guis": True
    }
    generators = "cmake", "cmake_find_package"
    exports_sources = "CMakeLists.txt"

    requires = (
        "fmt/[>=7.1.3]",
        "boost/[>=1.74.0]",
        "cxxopts/[>=2.2.1]",
        "gsl-lite/[>=0.37.0]",
        "openexr/[>=2.5.3 <3]",
        "outcome/[>=2.1.5]",
        "spdlog/[>=1.8.2]",
        "gtest/[>=1.10.0]",
        "onetbb/2020.3",
        "zlib/[>=1.2.11]",
        "alembic/1.7.16@blackencino/latest"
    )

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        self.options["onetbb"].shared = False

        if self.options.build_guis:
            self.requires.add("glfw/[>=3.3.2]")
            self.requires.add("imgui/[>=1.79]")
            self.requires.add("glad/[>=0.1.34]")

            #self.options["glfw"].fPIC = True
            #self.options["imgui"].fPIC = True

            self.options["glad"].shared = False
            #self.options["glad"].fPIC = True
            self.options["glad"].spec = "gl"
            self.options["glad"].no_loader = False
            self.options["glad"].gl_profile = "core"
            self.options["glad"].gl_version = "4.1"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("emerald-{}".format(self.version), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["EMERALD_BUILD_GUIS"] = self.options.build_guis
        self._cmake.definitions["EMERALD_DO_TESTS"] = False

        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        #tools.rmdir(os.path.join(self.package_folder, "share"))
        #tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        #tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "emerald"
        self.cpp_info.names["cmake_find_package_multi"] = "emerald"
        self.cpp_info.names["pkg_config"] = "emerald"

        self.cpp_info.libs = tools.collect_libs(self)







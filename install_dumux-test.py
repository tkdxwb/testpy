##!/usr/bin/env python3

'''
This script installs the module dumux-test together with all dependencies.
'''

import os
import subprocess


def show_message(message):
    print("*" * 120)
    print(message)
    print("*" * 120 + "\n")


# execute a command in a folder and retrieve the output
def runCommandFromPath(command, path="."):
    curPath = os.getcwd()
    os.chdir(path)
    subprocess.run(command)
    os.chdir(curPath)


def git_clone(url):
    clone = ["git", "clone"]
    runCommandFromPath(command=[*clone, url])


def git_setbranch(branch):
    checkout = ["git", "checkout", branch]
    runCommandFromPath(command=checkout)


def git_setrevision(sha):
    reset = ["git", "reset", "--hard", sha]
    runCommandFromPath(command=reset)


def git_apply_patch(folder, patch):
    apply = ["git", "apply", patch]
    runCommandFromPath(command=apply, path=folder)


def installModule(urls, deps):
    for url in urls:
        git_clone(url)
    for folder, branch, sha in zip(deps["folders"], deps["branches"], deps["shas"]):
        os.chdir(folder)
        git_setbranch(branch)
        git_setrevision(sha)
        os.chdir("..")


def applyPatch(patches):
    for folder, patch in zip(patches["folders"], patches["files"]):
        git_apply_patch(folder, patch)


if __name__ == '__main__':
    ###########################################################################
    # (1/3) Clone repositories, set branches and commits
    ###########################################################################
    show_message("(1/3) Cloning repositories, setting branches and commits...")
    urls = [
        "https://gitlab.dune-project.org/extensions/dune-alugrid",
        "https://gitlab.dune-project.org/core/dune-istl.git",
        "https://gitlab.dune-project.org/core/dune-grid.git",
        "https://gitlab.dune-project.org/core/dune-localfunctions.git",
        "https://gitlab.dune-project.org/core/dune-geometry.git",
        "https://gitlab.dune-project.org/extensions/dune-foamgrid.git",
        "https://gitlab.dune-project.org/core/dune-common.git",
        ]
    deps = {}
    deps["folders"] = [
        "dune-alugrid",
        "dune-istl",
        "dune-grid",
        "dune-localfunctions",
        "dune-geometry",
        "dune-foamgrid",
        "dune-common",
        ]
    deps["branches"] = [
        "origin/releases/2.7",
        "origin/releases/2.7",
        "origin/releases/2.7",
        "origin/releases/2.7",
        "origin/releases/2.7",
        "origin/master",
        "origin/master",
        ]
    deps["shas"] = [
        "178a69b69eca8bf3e31ddce0fd8c990fee4931ae",
        "761b28aa1deaa786ec55584ace99667545f1b493",
        "b7741c6599528bc42017e25f70eb6dd3b5780277",
        "68f1bcf32d9068c258707d241624a08b771b6fde",
        "9d56be3e286bc761dd5d453332a8d793eff00cbe",
        "d49187be4940227c945ced02f8457ccc9d47536a",
        "fae77c751103bd6effa9d215ffc4c32b434e0ae4",
        ]
    installModule(urls, deps)
    show_message("(1/3) Repositories are cloned and set properly.")
    ###########################################################################
    # (2/3) Generate and apply patches
    ###########################################################################
    show_message("(2/3) Creating patches for unpublished commits and uncommitted changes...")
    with open('dune-common/unpublished.patch', 'w') as patchFile:
        patchFile.write("""From c9c494d00241922f25c2fc8a0089f0c00e9c662a Mon Sep 17 00:00:00 2001
From: =?UTF-8?q?Christoph=20Gr=C3=BCninger?= <gruenich@dune-project.org>
Date: Wed, 20 Jan 2021 20:35:05 +0100
Subject: [PATCH 1/3] [cmake] Use FindPython3 from CMake 3.19.3

---
 cmake/modules/FindPython3/FindPython3.cmake | 115 +++-----------------
 cmake/modules/FindPython3/Support.cmake     |  77 ++++---------
 2 files changed, 33 insertions(+), 159 deletions(-)

diff --git a/cmake/modules/FindPython3/FindPython3.cmake b/cmake/modules/FindPython3/FindPython3.cmake
index 506a643f..c79d482d 100644
--- a/cmake/modules/FindPython3/FindPython3.cmake
+++ b/cmake/modules/FindPython3/FindPython3.cmake
@@ -10,32 +10,25 @@ FindPython3
 Find Python 3 interpreter, compiler and development environment (include
 directories and libraries).
 
-.. versionadded:: 3.19
-  When a version is requested, it can be specified as a simple value or as a
-  range. For a detailed description of version range usage and capabilities,
-  refer to the :command:`find_package` command.
+When a version is requested, it can be specified as a simple value or as a
+range. For a detailed description of version range usage and capabilities,
+refer to the :command:`find_package` command.
 
 The following components are supported:
 
 * ``Interpreter``: search for Python 3 interpreter
 * ``Compiler``: search for Python 3 compiler. Only offered by IronPython.
 * ``Development``: search for development artifacts (include directories and
-  libraries).
+  libraries). This component includes two sub-components which can be specified
+  independently:
 
-  .. versionadded:: 3.18
-    This component includes two sub-components which can be specified
-    independently:
-
-    * ``Development.Module``: search for artifacts for Python 3 module
-      developments.
-    * ``Development.Embed``: search for artifacts for Python 3 embedding
-      developments.
+  * ``Development.Module``: search for artifacts for Python 3 module
+    developments.
+  * ``Development.Embed``: search for artifacts for Python 3 embedding
+    developments.
 
 * ``NumPy``: search for NumPy include directories.
 
-.. versionadded:: 3.14
-  Added the ``NumPy`` component.
-
 If no ``COMPONENTS`` are specified, ``Interpreter`` is assumed.
 
 If component ``Development`` is specified, it implies sub-components
@@ -64,30 +57,20 @@ for you.
 Imported Targets
 ^^^^^^^^^^^^^^^^
 
-This module defines the following :ref:`Imported Targets <Imported Targets>`:
-
-.. versionchanged:: 3.14
-  :ref:`Imported Targets <Imported Targets>` are only created when
-  :prop_gbl:`CMAKE_ROLE` is ``PROJECT``.
+This module defines the following :ref:`Imported Targets <Imported Targets>`
+(when :prop_gbl:`CMAKE_ROLE` is ``PROJECT``):
 
 ``Python3::Interpreter``
   Python 3 interpreter. Target defined if component ``Interpreter`` is found.
 ``Python3::Compiler``
   Python 3 compiler. Target defined if component ``Compiler`` is found.
-
 ``Python3::Module``
-  .. versionadded:: 3.15
-
   Python 3 library for Python module. Target defined if component
   ``Development.Module`` is found.
-
 ``Python3::Python``
   Python 3 library for Python embedding. Target defined if component
   ``Development.Embed`` is found.
-
 ``Python3::NumPy``
-  .. versionadded:: 3.14
-
   NumPy library for Python 3. Target defined if component ``NumPy`` is found.
 
 Result Variables
@@ -134,10 +117,7 @@ This module will set the following variables in your project
   Information returned by
   ``distutils.sysconfig.get_python_lib(plat_specific=True,standard_lib=False)``
   or else ``sysconfig.get_path(\'platlib\')``.
-
 ``Python3_SOABI``
-  .. versionadded:: 3.17
-
   Extension suffix for modules.
 
   Information returned by
@@ -146,7 +126,6 @@ This module will set the following variables in your project
   ``python3-config --extension-suffix``. If package ``distutils.sysconfig`` is
   not available, ``sysconfig.get_config_var(\'SOABI\')`` or
   ``sysconfig.get_config_var(\'EXT_SUFFIX\')`` are used.
-
 ``Python3_Compiler_FOUND``
   System has the Python 3 compiler.
 ``Python3_COMPILER``
@@ -154,36 +133,19 @@ This module will set the following variables in your project
 ``Python3_COMPILER_ID``
   A short string unique to the compiler. Possible values include:
     * IronPython
-
 ``Python3_DOTNET_LAUNCHER``
-  .. versionadded:: 3.18
-
   The ``.Net`` interpreter. Only used by ``IronPython`` implementation.
-
 ``Python3_Development_FOUND``
-
   System has the Python 3 development artifacts.
-
 ``Python3_Development.Module_FOUND``
-  .. versionadded:: 3.18
-
   System has the Python 3 development artifacts for Python module.
-
 ``Python3_Development.Embed_FOUND``
-  .. versionadded:: 3.18
-
   System has the Python 3 development artifacts for Python embedding.
-
 ``Python3_INCLUDE_DIRS``
-
   The Python 3 include directories.
-
 ``Python3_LINK_OPTIONS``
-  .. versionadded:: 3.19
-
   The Python 3 link options. Some configurations require specific link options
   for a correct build and execution.
-
 ``Python3_LIBRARIES``
   The Python 3 libraries.
 ``Python3_LIBRARY_DIRS``
@@ -198,25 +160,13 @@ This module will set the following variables in your project
   Python 3 minor version.
 ``Python3_VERSION_PATCH``
   Python 3 patch version.
-
 ``Python3_PyPy_VERSION``
-  .. versionadded:: 3.18
-
   Python 3 PyPy version.
-
 ``Python3_NumPy_FOUND``
-  .. versionadded:: 3.14
-
   System has the NumPy.
-
 ``Python3_NumPy_INCLUDE_DIRS``
-  .. versionadded:: 3.14
-
   The NumPy include directories.
-
 ``Python3_NumPy_VERSION``
-  .. versionadded:: 3.14
-
   The NumPy version.
 
 Hints
@@ -232,8 +182,6 @@ Hints
   * If set to FALSE, search **only** for shared libraries.
 
 ``Python3_FIND_ABI``
-  .. versionadded:: 3.16
-
   This variable defines which ABIs, as defined in
   `PEP 3149 <https://www.python.org/dev/peps/pep-3149/>`_, should be searched.
 
@@ -275,8 +223,6 @@ Hints
     each flag is ``OFF`` or ``ANY``.
 
 ``Python3_FIND_STRATEGY``
-  .. versionadded:: 3.15
-
   This variable defines how lookup will be done.
   The ``Python3_FIND_STRATEGY`` variable can be set to one of the following:
 
@@ -289,8 +235,6 @@ Hints
     This is the default if policy :policy:`CMP0094` is set to ``NEW``.
 
 ``Python3_FIND_REGISTRY``
-  .. versionadded:: 3.13
-
   On Windows the ``Python3_FIND_REGISTRY`` variable determine the order
   of preference between registry and environment variables.
   The ``Python3_FIND_REGISTRY`` variable can be set to one of the following:
@@ -301,8 +245,6 @@ Hints
   * ``NEVER``: Never try to use registry.
 
 ``Python3_FIND_FRAMEWORK``
-  .. versionadded:: 3.15
-
   On macOS the ``Python3_FIND_FRAMEWORK`` variable determine the order of
   preference between Apple-style and unix-style package components.
   This variable can take same values as :variable:`CMAKE_FIND_FRAMEWORK`
@@ -316,8 +258,6 @@ Hints
   variable will be used, if any.
 
 ``Python3_FIND_VIRTUALENV``
-  .. versionadded:: 3.15
-
   This variable defines the handling of virtual environments managed by
   ``virtualenv`` or ``conda``. It is meaningful only when a virtual environment
   is active (i.e. the ``activate`` script has been evaluated). In this case, it
@@ -336,9 +276,6 @@ Hints
     ``NEVER`` to select preferably the interpreter from the virtual
     environment.
 
-  .. versionadded:: 3.17
-    Added support for ``conda`` environments.
-
   .. note::
 
     If the component ``Development`` is requested, it is **strongly**
@@ -346,8 +283,6 @@ Hints
     result.
 
 ``Python3_FIND_IMPLEMENTATIONS``
-  .. versionadded:: 3.18
-
   This variable defines, in an ordered list, the different implementations
   which will be searched. The ``Python3_FIND_IMPLEMENTATIONS`` variable can
   hold the following values:
@@ -380,26 +315,9 @@ Hints
     ``.Net`` interpreter (i.e. ``mono`` command) is expected to be available
     through the ``PATH`` variable.
 
-``Python3_FIND_UNVERSIONED_NAMES``
-  .. versionadded:: 3.20
-
-  This variable defines how the generic names will be searched. Currently, it
-  only applies to the generic names of the interpreter, namely, ``python3`` and
-  ``python``.
-  The ``Python3_FIND_UNVERSIONED_NAMES`` variable can be set to one of the
-  following values:
-
-  * ``FIRST``: The generic names are searched before the more specialized ones
-    (such as ``python3.5`` for example).
-  * ``LAST``: The generic names are searched after the more specialized ones.
-    This is the default.
-  * ``NEVER``: The generic name are not searched at all.
-
 Artifacts Specification
 ^^^^^^^^^^^^^^^^^^^^^^^
 
-.. versionadded:: 3.16
-
 To solve special cases, it is possible to specify directly the artifacts by
 setting the following variables:
 
@@ -410,8 +328,6 @@ setting the following variables:
   The path to the compiler.
 
 ``Python3_DOTNET_LAUNCHER``
-  .. versionadded:: 3.18
-
   The ``.Net`` interpreter. Only used by ``IronPython`` implementation.
 
 ``Python3_LIBRARY``
@@ -448,8 +364,6 @@ specification. So, to enable also interactive specification, module behavior
 can be controlled with the following variable:
 
 ``Python3_ARTIFACTS_INTERACTIVE``
-  .. versionadded:: 3.18
-
   Selects the behavior of the module. This is a boolean variable:
 
   * If set to ``TRUE``: Create CMake cache entries for the above artifact
@@ -472,9 +386,8 @@ of Python module naming rules::
 
 If the library type is not specified, ``MODULE`` is assumed.
 
-.. versionadded:: 3.17
-  For ``MODULE`` library type, if option ``WITH_SOABI`` is specified, the
-  module suffix will include the ``Python3_SOABI`` value, if any.
+For ``MODULE`` library type, if option ``WITH_SOABI`` is specified, the
+module suffix will include the ``Python3_SOABI`` value, if any.
 #]=======================================================================]
 
 
@@ -482,7 +395,7 @@ set (_PYTHON_PREFIX Python3)
 
 set (_Python3_REQUIRED_VERSION_MAJOR 3)
 
-include (${CMAKE_CURRENT_LIST_DIR}/Support.cmake)
+include (${CMAKE_CURRENT_LIST_DIR}/FindPython/Support.cmake)
 
 if (COMMAND __Python3_add_library)
   macro (Python3_add_library)
diff --git a/cmake/modules/FindPython3/Support.cmake b/cmake/modules/FindPython3/Support.cmake
index bf9cec51..79b1d184 100644
--- a/cmake/modules/FindPython3/Support.cmake
+++ b/cmake/modules/FindPython3/Support.cmake
@@ -31,7 +31,7 @@ endif()
 
 get_property(_${_PYTHON_PREFIX}_CMAKE_ROLE GLOBAL PROPERTY CMAKE_ROLE)
 
-include (FindPackageHandleStandardArgs)
+include (${CMAKE_CURRENT_LIST_DIR}/../FindPackageHandleStandardArgs.cmake)
 
 #
 # helper commands
@@ -99,9 +99,7 @@ macro (_PYTHON_FIND_FRAMEWORKS)
                          ~/Library/Frameworks
                          /usr/local/Frameworks
                          ${CMAKE_SYSTEM_FRAMEWORK_PATH})
-    if (_pff_frameworks) # Behavior change in CMake 3.14
-      list (REMOVE_DUPLICATES _pff_frameworks)
-    endif ()
+    list (REMOVE_DUPLICATES _pff_frameworks)
     foreach (_pff_implementation IN LISTS _${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS)
       unset (_${_PYTHON_PREFIX}_${_pff_implementation}_FRAMEWORKS)
       if (_pff_implementation STREQUAL \"CPython\")
@@ -323,9 +321,7 @@ function (_PYTHON_GET_PATH_SUFFIXES _PYTHON_PGPS_PATH_SUFFIXES)
       endif()
     endif()
   endforeach()
-  if (path_suffixes) # Behavior change in CMake 3.14
-    list (REMOVE_DUPLICATES path_suffixes)
-  endif ()
+  list (REMOVE_DUPLICATES path_suffixes)
 
   set (${_PYTHON_PGPS_PATH_SUFFIXES} ${path_suffixes} PARENT_SCOPE)
 endfunction()
@@ -341,9 +337,6 @@ function (_PYTHON_GET_NAMES _PYTHON_PGN_NAMES)
 
   foreach (implementation IN LISTS _PGN_IMPLEMENTATIONS)
     if (implementation STREQUAL \"CPython\")
-      if (_PGN_INTERPRETER AND _${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES STREQUAL \"FIRST\")
-        list (APPEND names python${_${_PYTHON_PREFIX}_REQUIRED_VERSION_MAJOR} python)
-      endif()
       foreach (version IN LISTS _PGN_VERSION)
         if (_PGN_WIN32)
           string (REPLACE \".\" \"\" version_no_dots ${version})
@@ -393,7 +386,7 @@ function (_PYTHON_GET_NAMES _PYTHON_PGN_NAMES)
           endif()
         endif()
       endforeach()
-      if (_PGN_INTERPRETER AND _${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES STREQUAL \"LAST\")
+      if (_PGN_INTERPRETER)
         list (APPEND names python${_${_PYTHON_PREFIX}_REQUIRED_VERSION_MAJOR} python)
       endif()
     elseif (implementation STREQUAL \"IronPython\")
@@ -457,9 +450,7 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
         # do some clean-up
         string (REGEX MATCHALL \"(-I|-iwithsysroot)[ ]*[^ ]+\" _values \"${_values}\")
         string (REGEX REPLACE \"(-I|-iwithsysroot)[ ]*\" \"\" _values \"${_values}\")
-        if (_values) # Behavior change in CMake 3.14
-          list (REMOVE_DUPLICATES _values)
-        endif ()
+        list (REMOVE_DUPLICATES _values)
       elseif (NAME STREQUAL \"SOABI\")
         # clean-up: remove prefix character and suffix
         if (_values MATCHES \"^(\\\\.${CMAKE_SHARED_LIBRARY_SUFFIX}|\\\\.so|\\\\.pyd)$\")
@@ -481,9 +472,7 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
       if (_result)
         unset (_values)
       else()
-        if (_values) # Behavior change in CMake 3.14
-          list (REMOVE_DUPLICATES _values)
-        endif ()
+        list (REMOVE_DUPLICATES _values)
       endif()
     elseif (NAME STREQUAL \"INCLUDES\")
       if (WIN32)
@@ -500,9 +489,7 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
       if (_result)
         unset (_values)
       else()
-        if (_values) # Behavior change in CMake 3.14
-          list (REMOVE_DUPLICATES _values)
-        endif ()
+        list (REMOVE_DUPLICATES _values)
       endif()
     elseif (NAME STREQUAL \"SOABI\")
       execute_process (COMMAND ${_${_PYTHON_PREFIX}_INTERPRETER_LAUNCHER} \"${_${_PYTHON_PREFIX}_EXECUTABLE}\" -c
@@ -560,9 +547,7 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
     string (REGEX MATCHALL \"-(l|framework)[ ]*[^ ]+\" _values \"${_values}\")
     # remove elements relative to python library itself
     list (FILTER _values EXCLUDE REGEX \"-lpython\")
-    if (_values) # Behavior change in CMake 3.14
-          list (REMOVE_DUPLICATES _values)
-        endif ()
+    list (REMOVE_DUPLICATES _values)
   endif()
 
   if (WIN32 AND NAME MATCHES \"^(PREFIX|CONFIGDIR|INCLUDES)$\")
@@ -1081,9 +1066,7 @@ function (_PYTHON_SET_LIBRARY_DIRS _PYTHON_SLD_RESULT)
       list (APPEND _PYTHON_DIRS \"${_PYTHON_DIR}\")
     endif()
   endforeach()
-  if (_PYTHON_DIRS) # Behavior change in CMake 3.14
-    list (REMOVE_DUPLICATES _PYTHON_DIRS)
-  endif ()
+  list (REMOVE_DUPLICATES _PYTHON_DIRS)
   set (${_PYTHON_SLD_RESULT} ${_PYTHON_DIRS} PARENT_SCOPE)
 endfunction()
 
@@ -1142,9 +1125,7 @@ endif()
 if (\"Development\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS)
   list (APPEND ${_PYTHON_PREFIX}_FIND_COMPONENTS \"Development.Module\" \"Development.Embed\")
 endif()
-if (${_PYTHON_PREFIX}_FIND_COMPONENTS) # Behavior change in CMake 3.14
-  list (REMOVE_DUPLICATES ${_PYTHON_PREFIX}_FIND_COMPONENTS)
-endif ()
+list (REMOVE_DUPLICATES ${_PYTHON_PREFIX}_FIND_COMPONENTS)
 foreach (_${_PYTHON_PREFIX}_COMPONENT IN ITEMS Interpreter Compiler Development Development.Module Development.Embed NumPy)
   set (${_PYTHON_PREFIX}_${_${_PYTHON_PREFIX}_COMPONENT}_FOUND FALSE)
 endforeach()
@@ -1166,9 +1147,7 @@ if (\"Development.Embed\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS)
   list (APPEND _${_PYTHON_PREFIX}_FIND_DEVELOPMENT_EMBED_ARTIFACTS \"LIBRARY\" \"INCLUDE_DIR\")
 endif()
 set (_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS ${_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_MODULE_ARTIFACTS} ${_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_EMBED_ARTIFACTS})
-if (_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS) # Behavior change in CMake 3.14
-  list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS)
-endif ()
+list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS)
 
 # Set versions to search
 ## default: search any version
@@ -1228,11 +1207,7 @@ endif()
 unset (${_PYTHON_PREFIX}_SOABI)
 
 # Define lookup strategy
-if(POLICY CMP0094)
-  cmake_policy (GET CMP0094 _${_PYTHON_PREFIX}_LOOKUP_POLICY)
-else()
-  set (_${_PYTHON_PREFIX}_LOOKUP_POLICY \"OLD\")
-endif()
+cmake_policy (GET CMP0094 _${_PYTHON_PREFIX}_LOOKUP_POLICY)
 if (_${_PYTHON_PREFIX}_LOOKUP_POLICY STREQUAL \"NEW\")
   set (_${_PYTHON_PREFIX}_FIND_STRATEGY \"LOCATION\")
 else()
@@ -1397,22 +1372,9 @@ else()
 endif()
 
 
-# Python naming handling
-if (DEFINED ${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES)
-  if (NOT ${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES MATCHES \"^(FIRST|LAST|NEVER)$\")
-    message (AUTHOR_WARNING \"Find${_PYTHON_PREFIX}: ${_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES}: invalid value for \'${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES\'. \'FIRST\', \'LAST\' or \'NEVER\' expected. \'LAST\' will be used instead.\")
-    set (_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES LAST)
-  else()
-    set (_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES ${${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES})
-  endif()
-else()
-  set (_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES LAST)
-endif()
-
-
 # Compute search signature
 # This signature will be used to check validity of cached variables on new search
-set (_${_PYTHON_PREFIX}_SIGNATURE \"${${_PYTHON_PREFIX}_ROOT_DIR}:${_${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS}:${_${_PYTHON_PREFIX}_FIND_STRATEGY}:${${_PYTHON_PREFIX}_FIND_VIRTUALENV}${_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES}\")
+set (_${_PYTHON_PREFIX}_SIGNATURE \"${${_PYTHON_PREFIX}_ROOT_DIR}:${_${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS}:${_${_PYTHON_PREFIX}_FIND_STRATEGY}:${${_PYTHON_PREFIX}_FIND_VIRTUALENV}\")
 if (NOT WIN32)
   string (APPEND _${_PYTHON_PREFIX}_SIGNATURE \":${${_PYTHON_PREFIX}_USE_STATIC_LIBS}:\")
 endif()
@@ -2332,9 +2294,7 @@ if (${_PYTHON_PREFIX}_FIND_REQUIRED_Development.Embed)
     list (APPEND _${_PYTHON_PREFIX}_REQUIRED_VARS ${_PYTHON_PREFIX}_INCLUDE_DIRS)
   endif()
 endif()
-if (_${_PYTHON_PREFIX}_REQUIRED_VARS) # Behavior change in CMake 3.14
-  list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_REQUIRED_VARS)
-endif ()
+list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_REQUIRED_VARS)
 ## Development environment is not compatible with IronPython interpreter
 if ((\"Development.Module\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS
       OR \"Development.Embed\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS)
@@ -3045,9 +3005,8 @@ if ((\"Development.Module\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS
     unset(_${_PYTHON_PREFIX}_is_prefix)
     foreach (_${_PYTHON_PREFIX}_implementation IN LISTS _${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS)
       foreach (_${_PYTHON_PREFIX}_framework IN LISTS _${_PYTHON_PREFIX}_${_${_PYTHON_PREFIX}_implementation}_FRAMEWORKS)
-        cmake_path (IS_PREFIX _${_PYTHON_PREFIX}_framework \"${${_PYTHON_PREFIX}_LIBRARY_RELEASE}\" _${_PYTHON_PREFIX}_is_prefix)
-        if (_${_PYTHON_PREFIX}_is_prefix)
-          cmake_path (GET _${_PYTHON_PREFIX}_framework PARENT_PATH _${_PYTHON_PREFIX}_framework)
+        if (${_PYTHON_PREFIX}_LIBRARY_RELEASE MATCHES \"^${_${_PYTHON_PREFIX}_framework}\")
+          get_filename_component (_${_PYTHON_PREFIX}_framework \"${_${_PYTHON_PREFIX}_framework}\" DIRECTORY)
           set (${_PYTHON_PREFIX}_LINK_OPTIONS \"LINKER:-rpath,${_${_PYTHON_PREFIX}_framework}\")
           break()
         endif()
@@ -3189,7 +3148,9 @@ endforeach()
 find_package_handle_standard_args (${_PYTHON_PREFIX}
                                    REQUIRED_VARS ${_${_PYTHON_PREFIX}_REQUIRED_VARS}
                                    VERSION_VAR ${_PYTHON_PREFIX}_VERSION
-                                   HANDLE_COMPONENTS)
+                                   HANDLE_VERSION_RANGE
+                                   HANDLE_COMPONENTS
+                                   REASON_FAILURE_MESSAGE \"${_${_PYTHON_PREFIX}_REASON_FAILURE}\")
 
 # Create imported targets and helper functions
 if(_${_PYTHON_PREFIX}_CMAKE_ROLE STREQUAL \"PROJECT\")
-- 
2.30.1 (Apple Git-130)


From 7b70ffaaa096aeeb04cfe5694334d5d56457f7c7 Mon Sep 17 00:00:00 2001
From: =?UTF-8?q?Christoph=20Gr=C3=BCninger?= <gruenich@dune-project.org>
Date: Wed, 20 Jan 2021 20:48:57 +0100
Subject: [PATCH 2/3] [CMake] Backport FindPython3 to CMake 3.13

* All known code constructs not supported by CMake 3.13
  are worked around
* Adjusted paths to match location in Dune
---
 cmake/modules/FindPython3/FindPython3.cmake |  2 +-
 cmake/modules/FindPython3/Support.cmake     | 52 +++++++++++++++------
 2 files changed, 38 insertions(+), 16 deletions(-)

diff --git a/cmake/modules/FindPython3/FindPython3.cmake b/cmake/modules/FindPython3/FindPython3.cmake
index c79d482d..da7b12d0 100644
--- a/cmake/modules/FindPython3/FindPython3.cmake
+++ b/cmake/modules/FindPython3/FindPython3.cmake
@@ -395,7 +395,7 @@ set (_PYTHON_PREFIX Python3)
 
 set (_Python3_REQUIRED_VERSION_MAJOR 3)
 
-include (${CMAKE_CURRENT_LIST_DIR}/FindPython/Support.cmake)
+include (${CMAKE_CURRENT_LIST_DIR}/Support.cmake)
 
 if (COMMAND __Python3_add_library)
   macro (Python3_add_library)
diff --git a/cmake/modules/FindPython3/Support.cmake b/cmake/modules/FindPython3/Support.cmake
index 79b1d184..cf3a121b 100644
--- a/cmake/modules/FindPython3/Support.cmake
+++ b/cmake/modules/FindPython3/Support.cmake
@@ -31,7 +31,7 @@ endif()
 
 get_property(_${_PYTHON_PREFIX}_CMAKE_ROLE GLOBAL PROPERTY CMAKE_ROLE)
 
-include (${CMAKE_CURRENT_LIST_DIR}/../FindPackageHandleStandardArgs.cmake)
+include (FindPackageHandleStandardArgs)
 
 #
 # helper commands
@@ -99,7 +99,9 @@ macro (_PYTHON_FIND_FRAMEWORKS)
                          ~/Library/Frameworks
                          /usr/local/Frameworks
                          ${CMAKE_SYSTEM_FRAMEWORK_PATH})
-    list (REMOVE_DUPLICATES _pff_frameworks)
+    if (_pff_frameworks) # Behavior change in CMake 3.14
+      list (REMOVE_DUPLICATES _pff_frameworks)
+    endif ()
     foreach (_pff_implementation IN LISTS _${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS)
       unset (_${_PYTHON_PREFIX}_${_pff_implementation}_FRAMEWORKS)
       if (_pff_implementation STREQUAL \"CPython\")
@@ -321,7 +323,9 @@ function (_PYTHON_GET_PATH_SUFFIXES _PYTHON_PGPS_PATH_SUFFIXES)
       endif()
     endif()
   endforeach()
-  list (REMOVE_DUPLICATES path_suffixes)
+  if (path_suffixes) # Behavior change in CMake 3.14
+    list (REMOVE_DUPLICATES path_suffixes)
+  endif ()
 
   set (${_PYTHON_PGPS_PATH_SUFFIXES} ${path_suffixes} PARENT_SCOPE)
 endfunction()
@@ -450,7 +454,9 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
         # do some clean-up
         string (REGEX MATCHALL \"(-I|-iwithsysroot)[ ]*[^ ]+\" _values \"${_values}\")
         string (REGEX REPLACE \"(-I|-iwithsysroot)[ ]*\" \"\" _values \"${_values}\")
-        list (REMOVE_DUPLICATES _values)
+        if (_values) # Behavior change in CMake 3.14
+          list (REMOVE_DUPLICATES _values)
+        endif ()
       elseif (NAME STREQUAL \"SOABI\")
         # clean-up: remove prefix character and suffix
         if (_values MATCHES \"^(\\\\.${CMAKE_SHARED_LIBRARY_SUFFIX}|\\\\.so|\\\\.pyd)$\")
@@ -472,7 +478,9 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
       if (_result)
         unset (_values)
       else()
-        list (REMOVE_DUPLICATES _values)
+        if (_values) # Behavior change in CMake 3.14
+          list (REMOVE_DUPLICATES _values)
+        endif ()
       endif()
     elseif (NAME STREQUAL \"INCLUDES\")
       if (WIN32)
@@ -489,7 +497,9 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
       if (_result)
         unset (_values)
       else()
-        list (REMOVE_DUPLICATES _values)
+        if (_values) # Behavior change in CMake 3.14
+          list (REMOVE_DUPLICATES _values)
+        endif ()
       endif()
     elseif (NAME STREQUAL \"SOABI\")
       execute_process (COMMAND ${_${_PYTHON_PREFIX}_INTERPRETER_LAUNCHER} \"${_${_PYTHON_PREFIX}_EXECUTABLE}\" -c
@@ -547,7 +557,9 @@ function (_PYTHON_GET_CONFIG_VAR _PYTHON_PGCV_VALUE NAME)
     string (REGEX MATCHALL \"-(l|framework)[ ]*[^ ]+\" _values \"${_values}\")
     # remove elements relative to python library itself
     list (FILTER _values EXCLUDE REGEX \"-lpython\")
-    list (REMOVE_DUPLICATES _values)
+    if (_values) # Behavior change in CMake 3.14
+          list (REMOVE_DUPLICATES _values)
+        endif ()
   endif()
 
   if (WIN32 AND NAME MATCHES \"^(PREFIX|CONFIGDIR|INCLUDES)$\")
@@ -1066,7 +1078,9 @@ function (_PYTHON_SET_LIBRARY_DIRS _PYTHON_SLD_RESULT)
       list (APPEND _PYTHON_DIRS \"${_PYTHON_DIR}\")
     endif()
   endforeach()
-  list (REMOVE_DUPLICATES _PYTHON_DIRS)
+  if (_PYTHON_DIRS) # Behavior change in CMake 3.14
+    list (REMOVE_DUPLICATES _PYTHON_DIRS)
+  endif ()
   set (${_PYTHON_SLD_RESULT} ${_PYTHON_DIRS} PARENT_SCOPE)
 endfunction()
 
@@ -1125,7 +1139,9 @@ endif()
 if (\"Development\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS)
   list (APPEND ${_PYTHON_PREFIX}_FIND_COMPONENTS \"Development.Module\" \"Development.Embed\")
 endif()
-list (REMOVE_DUPLICATES ${_PYTHON_PREFIX}_FIND_COMPONENTS)
+if (${_PYTHON_PREFIX}_FIND_COMPONENTS) # Behavior change in CMake 3.14
+  list (REMOVE_DUPLICATES ${_PYTHON_PREFIX}_FIND_COMPONENTS)
+endif ()
 foreach (_${_PYTHON_PREFIX}_COMPONENT IN ITEMS Interpreter Compiler Development Development.Module Development.Embed NumPy)
   set (${_PYTHON_PREFIX}_${_${_PYTHON_PREFIX}_COMPONENT}_FOUND FALSE)
 endforeach()
@@ -1147,7 +1163,9 @@ if (\"Development.Embed\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS)
   list (APPEND _${_PYTHON_PREFIX}_FIND_DEVELOPMENT_EMBED_ARTIFACTS \"LIBRARY\" \"INCLUDE_DIR\")
 endif()
 set (_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS ${_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_MODULE_ARTIFACTS} ${_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_EMBED_ARTIFACTS})
-list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS)
+if (_${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS) # Behavior change in CMake 3.14
+  list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_FIND_DEVELOPMENT_ARTIFACTS)
+endif ()
 
 # Set versions to search
 ## default: search any version
@@ -1207,7 +1225,11 @@ endif()
 unset (${_PYTHON_PREFIX}_SOABI)
 
 # Define lookup strategy
-cmake_policy (GET CMP0094 _${_PYTHON_PREFIX}_LOOKUP_POLICY)
+if(POLICY CMP0094)
+  cmake_policy (GET CMP0094 _${_PYTHON_PREFIX}_LOOKUP_POLICY)
+else()
+  set (_${_PYTHON_PREFIX}_LOOKUP_POLICY \"OLD\")
+endif()
 if (_${_PYTHON_PREFIX}_LOOKUP_POLICY STREQUAL \"NEW\")
   set (_${_PYTHON_PREFIX}_FIND_STRATEGY \"LOCATION\")
 else()
@@ -2294,7 +2316,9 @@ if (${_PYTHON_PREFIX}_FIND_REQUIRED_Development.Embed)
     list (APPEND _${_PYTHON_PREFIX}_REQUIRED_VARS ${_PYTHON_PREFIX}_INCLUDE_DIRS)
   endif()
 endif()
-list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_REQUIRED_VARS)
+if (_${_PYTHON_PREFIX}_REQUIRED_VARS) # Behavior change in CMake 3.14
+  list (REMOVE_DUPLICATES _${_PYTHON_PREFIX}_REQUIRED_VARS)
+endif ()
 ## Development environment is not compatible with IronPython interpreter
 if ((\"Development.Module\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS
       OR \"Development.Embed\" IN_LIST ${_PYTHON_PREFIX}_FIND_COMPONENTS)
@@ -3148,9 +3172,7 @@ endforeach()
 find_package_handle_standard_args (${_PYTHON_PREFIX}
                                    REQUIRED_VARS ${_${_PYTHON_PREFIX}_REQUIRED_VARS}
                                    VERSION_VAR ${_PYTHON_PREFIX}_VERSION
-                                   HANDLE_VERSION_RANGE
-                                   HANDLE_COMPONENTS
-                                   REASON_FAILURE_MESSAGE \"${_${_PYTHON_PREFIX}_REASON_FAILURE}\")
+                                   HANDLE_COMPONENTS)
 
 # Create imported targets and helper functions
 if(_${_PYTHON_PREFIX}_CMAKE_ROLE STREQUAL \"PROJECT\")
-- 
2.30.1 (Apple Git-130)


From d07215f0a9700c7df44572e191728767586c7e48 Mon Sep 17 00:00:00 2001
From: =?UTF-8?q?Christoph=20Gr=C3=BCninger?= <gruenich@dune-project.org>
Date: Wed, 20 Jan 2021 20:53:46 +0100
Subject: [PATCH 3/3] [cmake] Backport FindPython3 support for unversioned
 Python

Enables searching first for \"unversioned\" Python symlinks
like python3 or python 3.9
---
 cmake/modules/FindPython3/FindPython3.cmake | 15 +++++++++++++++
 cmake/modules/FindPython3/Support.cmake     | 20 ++++++++++++++++++--
 2 files changed, 33 insertions(+), 2 deletions(-)

diff --git a/cmake/modules/FindPython3/FindPython3.cmake b/cmake/modules/FindPython3/FindPython3.cmake
index da7b12d0..ff3c43d8 100644
--- a/cmake/modules/FindPython3/FindPython3.cmake
+++ b/cmake/modules/FindPython3/FindPython3.cmake
@@ -315,6 +315,21 @@ Hints
     ``.Net`` interpreter (i.e. ``mono`` command) is expected to be available
     through the ``PATH`` variable.
 
+``Python3_FIND_UNVERSIONED_NAMES``
+  .. versionadded:: 3.20
+
+  This variable defines how the generic names will be searched. Currently, it
+  only applies to the generic names of the interpreter, namely, ``python3`` and
+  ``python``.
+  The ``Python3_FIND_UNVERSIONED_NAMES`` variable can be set to one of the
+  following values:
+
+  * ``FIRST``: The generic names are searched before the more specialized ones
+    (such as ``python3.5`` for example).
+  * ``LAST``: The generic names are searched after the more specialized ones.
+    This is the default.
+  * ``NEVER``: The generic name are not searched at all.
+
 Artifacts Specification
 ^^^^^^^^^^^^^^^^^^^^^^^
 
diff --git a/cmake/modules/FindPython3/Support.cmake b/cmake/modules/FindPython3/Support.cmake
index cf3a121b..d92ec062 100644
--- a/cmake/modules/FindPython3/Support.cmake
+++ b/cmake/modules/FindPython3/Support.cmake
@@ -341,6 +341,9 @@ function (_PYTHON_GET_NAMES _PYTHON_PGN_NAMES)
 
   foreach (implementation IN LISTS _PGN_IMPLEMENTATIONS)
     if (implementation STREQUAL \"CPython\")
+      if (_PGN_INTERPRETER AND _${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES STREQUAL \"FIRST\")
+        list (APPEND names python${_${_PYTHON_PREFIX}_REQUIRED_VERSION_MAJOR} python)
+      endif()
       foreach (version IN LISTS _PGN_VERSION)
         if (_PGN_WIN32)
           string (REPLACE \".\" \"\" version_no_dots ${version})
@@ -390,7 +393,7 @@ function (_PYTHON_GET_NAMES _PYTHON_PGN_NAMES)
           endif()
         endif()
       endforeach()
-      if (_PGN_INTERPRETER)
+      if (_PGN_INTERPRETER AND _${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES STREQUAL \"LAST\")
         list (APPEND names python${_${_PYTHON_PREFIX}_REQUIRED_VERSION_MAJOR} python)
       endif()
     elseif (implementation STREQUAL \"IronPython\")
@@ -1394,9 +1397,22 @@ else()
 endif()
 
 
+# Python naming handling
+if (DEFINED ${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES)
+  if (NOT ${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES MATCHES \"^(FIRST|LAST|NEVER)$\")
+    message (AUTHOR_WARNING \"Find${_PYTHON_PREFIX}: ${_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES}: invalid value for \'${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES\'. \'FIRST\', \'LAST\' or \'NEVER\' expected. \'LAST\' will be used instead.\")
+    set (_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES LAST)
+  else()
+    set (_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES ${${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES})
+  endif()
+else()
+  set (_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES LAST)
+endif()
+
+
 # Compute search signature
 # This signature will be used to check validity of cached variables on new search
-set (_${_PYTHON_PREFIX}_SIGNATURE \"${${_PYTHON_PREFIX}_ROOT_DIR}:${_${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS}:${_${_PYTHON_PREFIX}_FIND_STRATEGY}:${${_PYTHON_PREFIX}_FIND_VIRTUALENV}\")
+set (_${_PYTHON_PREFIX}_SIGNATURE \"${${_PYTHON_PREFIX}_ROOT_DIR}:${_${_PYTHON_PREFIX}_FIND_IMPLEMENTATIONS}:${_${_PYTHON_PREFIX}_FIND_STRATEGY}:${${_PYTHON_PREFIX}_FIND_VIRTUALENV}${_${_PYTHON_PREFIX}_FIND_UNVERSIONED_NAMES}\")
 if (NOT WIN32)
   string (APPEND _${_PYTHON_PREFIX}_SIGNATURE \":${${_PYTHON_PREFIX}_USE_STATIC_LIBS}:\")
 endif()
-- 
2.30.1 (Apple Git-130)

""" )
    show_message("(2/3) Applying patches for unpublished commits and uncommitted changes...")
    patches = {}
    patches["folders"] = [
        "dune-common",
        ]
    patches["files"] = [
        "unpublished.patch",
        ]
    applyPatch(patches)

    show_message("(2/3) Step completed. All patch files are generated and applied.")
    ###########################################################################
    # (3/3) Configure and build
    ###########################################################################
    show_message("(3/3) Configure and build dune modules and dumux using dunecontrol....")
    runCommandFromPath(command=["./dune-common/bin/dunecontrol", "--opts=dumux/cmake.opts", "all"])
    os.chdir("dumux-test/build-cmake")
    runCommandFromPath(command=["make", "build_tests"])
    show_message("(3/3) Step completed. Succesfully configured and built tests.")

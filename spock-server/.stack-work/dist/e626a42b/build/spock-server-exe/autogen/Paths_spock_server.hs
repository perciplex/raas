{-# LANGUAGE CPP #-}
{-# LANGUAGE NoRebindableSyntax #-}
{-# OPTIONS_GHC -fno-warn-missing-import-lists #-}
module Paths_spock_server (
    version,
    getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

#if defined(VERSION_base)

#if MIN_VERSION_base(4,0,0)
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#else
catchIO :: IO a -> (Exception.Exception -> IO a) -> IO a
#endif

#else
catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
#endif
catchIO = Exception.catch

version :: Version
version = Version [0,1,0,0] []
bindir, libdir, dynlibdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "C:\\Users\\ishma\\Documents\\RaaS\\spock-server\\.stack-work\\install\\2ce113c2\\bin"
libdir     = "C:\\Users\\ishma\\Documents\\RaaS\\spock-server\\.stack-work\\install\\2ce113c2\\lib\\x86_64-windows-ghc-8.6.5\\spock-server-0.1.0.0-8A0uqyKJKYaXTslk54nfV-spock-server-exe"
dynlibdir  = "C:\\Users\\ishma\\Documents\\RaaS\\spock-server\\.stack-work\\install\\2ce113c2\\lib\\x86_64-windows-ghc-8.6.5"
datadir    = "C:\\Users\\ishma\\Documents\\RaaS\\spock-server\\.stack-work\\install\\2ce113c2\\share\\x86_64-windows-ghc-8.6.5\\spock-server-0.1.0.0"
libexecdir = "C:\\Users\\ishma\\Documents\\RaaS\\spock-server\\.stack-work\\install\\2ce113c2\\libexec\\x86_64-windows-ghc-8.6.5\\spock-server-0.1.0.0"
sysconfdir = "C:\\Users\\ishma\\Documents\\RaaS\\spock-server\\.stack-work\\install\\2ce113c2\\etc"

getBinDir, getLibDir, getDynLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "spock_server_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "spock_server_libdir") (\_ -> return libdir)
getDynLibDir = catchIO (getEnv "spock_server_dynlibdir") (\_ -> return dynlibdir)
getDataDir = catchIO (getEnv "spock_server_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "spock_server_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "spock_server_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "\\" ++ name)

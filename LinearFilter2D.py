import numpy              as np
import numpy.ctypeslib    as Flib
import ctypes, sys
import os.path
import myStyle.LoadConfig as lcf

# ======================================== #
# ===   Fortran 関数 呼び出しラッパ    === #
# ======================================== #
def LinearFilter2D( Data  =None, alpha =None, coordinate=None   , config=None, nFilter=1, \
                    x1Axis=None, x2Axis=None, dx1=None, dx2=None, x1Min =None, x2Min  =None ):
    # ---------------------------------------- #
    # --- [1]        引数チェック          --- #
    # ---------------------------------------- #
    if ( config     is None ): config     = lcf.LoadConfig()
    if ( Data       is None ): sys.exit( "[fLIB__LinearFilter2D] v1 ???" )
    if ( alpha      is None ): alpha      = config["cmp_LinearFilt"]
    if ( coordinate is None ): coordinate = config["Coordinate"]
    LI, LJ   = Data.shape[1], Data.shape[0]
    ret      = np.zeros( ( LJ,LI ) )

    # ---------------------------------------- #
    # --- [2]      ライブラリをロード      --- #
    # ---------------------------------------- #
    #  -- [2-1] ライブラリを定義 --  #
    path   = os.path.expanduser('~') + "/.python/lib/nkFilterRoutines/"
    pyLIB  = Flib.load_library( 'pylib.so', path )
    # ---------------------------------------- #
    # --- [3]      xyz 座標系              --- #
    # ---------------------------------------- #
    if ( coordinate=="xyz" ):
        #  -- [3-1] 入出力管理       --  #
        pyLIB.linearfilter2d_.argtypes = [
            Flib.ndpointer( dtype=np.float64 ),
            Flib.ndpointer( dtype=np.float64 ),
            Flib.ndpointer( dtype=np.float64 ),
            ctypes.POINTER( ctypes.c_int64   ),
            ctypes.POINTER( ctypes.c_int64   )
        ]
        pyLIB.linearfilter2d_.restype = ctypes.c_void_p
        #  -- [3-2] Fortranサイズへ  --  #
        Data_  =     np.array( Data  , dtype=np.float64 )
        ret_   =     np.array( ret   , dtype=np.float64 )
        alpha_ =     np.array( alpha , dtype=np.float64 )
        LI_    = ctypes.byref( ctypes.c_int64( LI   )   )
        LJ_    = ctypes.byref( ctypes.c_int64( LJ   )   )

        # ---------------------------------------- #
        # --- [4]       関数呼出 / 返却        --- #
        # ---------------------------------------- #
        pyLIB.linearfilter2d_( Data_, ret_, alpha_, LI_, LJ_ )
    elif ( coordinate=="rtz" ):
        #  -- [4-1] 座標軸準備       --  #
        if ( x1Axis is None ): x1Axis = dx1*np.arange( LI ) + x1Min
        if ( x2Axis is None ): x2Axis = dx2*np.arange( LJ ) + x2Min
        #  -- [4-2] 入出力管理       --  #
        pyLIB.cyllinearfilter2d_.argtypes = [
            Flib.ndpointer( dtype=np.float64 ),
            Flib.ndpointer( dtype=np.float64 ),
            Flib.ndpointer( dtype=np.float64 ),
            Flib.ndpointer( dtype=np.float64 ),
            Flib.ndpointer( dtype=np.float64 ),
            ctypes.POINTER( ctypes.c_int64   ),
            ctypes.POINTER( ctypes.c_int64   )
        ]
        pyLIB.cyllinearfilter2d_.restype = ctypes.c_void_p
        #  -- [4-3] Fortranサイズへ  --  #
        Data_  =     np.array( Data  , dtype=np.float64 )
        ret_   =     np.array( ret   , dtype=np.float64 )
        x1a_   =     np.array( x1Axis, dtype=np.float64 )
        x2a_   =     np.array( x2Axis, dtype=np.float64 )
        alpha_ =     np.array( alpha , dtype=np.float64 )
        LI_    = ctypes.byref( ctypes.c_int64( LI   )   )
        LJ_    = ctypes.byref( ctypes.c_int64( LJ   )   )

        # ---------------------------------------- #
        # --- [5]       関数呼出 / 返却        --- #
        # ---------------------------------------- #
        pyLIB.cyllinearfilter2d_( Data_, ret_, x1a_, x2a_, alpha_, LI_, LJ_ )
    else:
        print( " coordinate = {0} ??  ".format( coordinate ) )
    return( ret_ )


# ======================================== #
# ===             テスト用             === #
# ======================================== #
if ( __name__=='__main__' ):
    # ---- テスト用 プロファイル ---- #
    # -- 座標系 xg, yg -- #
    import myBasicAlgs.dist as dist
    Data = dist.dist( 21,21 )
    ret  = LinearFilter2D( Data=Data )
    import myStyle.cMap2D as clm
    clm.cMap2D( cMap=Data, FigName="Data.png" )
    clm.cMap2D( cMap=ret, FigName="ret.png" )
    print( Data.shape, ret.shape )

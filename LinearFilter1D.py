import numpy              as np
import numpy.ctypeslib    as Flib
import ctypes, sys
import os.path
import myStyle.LoadConfig as lcf

# ======================================== #
# ===   Fortran 関数 呼び出しラッパ    === #
# ======================================== #
def LinearFilter1D( Data=None, alpha=None, nFilter=None, config=None ):
    # ---------------------------------------- #
    # --- [1]        引数チェック          --- #
    # ---------------------------------------- #
    if ( Data       is None ): sys.exit( "[fLIB__LinearFilter1D] Data= ??" )
    if ( config     is None ): config  = lcf.LoadConfig()
    if ( alpha      is None ): alpha   = config["plt_LinearFilt"]
    if ( nFilter    is None ): nFilter = 1
    LI  = Data.shape[0]
    ret = np.zeros( ( LI ) )

    # ---------------------------------------- #
    # --- [2]      ライブラリをロード      --- #
    # ---------------------------------------- #
    #  -- [2-1] ライブラリを定義           --  #
    path   = os.path.expanduser('~') + "/.python/lib/nkFilterRoutines/"
    pyLIB  = Flib.load_library( 'pylib.so', path )
    #  -- [2-2] 入出力管理       --  #
    pyLIB.linearfilter1d_.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   )
    ]
    pyLIB.linearfilter1d_.restype = ctypes.c_void_p
    #  -- [2-3] Fortranサイズへ  --  #
    Data_    =     np.array( Data  , dtype=np.float64  )
    ret_     =     np.array( ret   , dtype=np.float64  )
    alpha_   =     np.array( alpha , dtype=np.float64  )
    nFilter_ = ctypes.byref( ctypes.c_int64( nFilter ) )
    LI_      = ctypes.byref( ctypes.c_int64( LI      ) )

    # ---------------------------------------- #
    # --- [3]       関数呼出 / 返却        --- #
    # ---------------------------------------- #
    pyLIB.linearfilter1d_( Data_, ret_, alpha_, nFilter_, LI_ )
    return( ret_ )


# ======================================== #
# ===             テスト用             === #
# ======================================== #
if ( __name__=='__main__' ):
    # ---- テスト用 プロファイル ---- #
    # -- 座標系 xg, yg -- #
    
    xa   = np.linspace( 0.0, 4.0*np.pi, 1000 ) 
    ya   = 1.0*np.sin( xa ) + 0.2*np.random.random( 1000 )
    
    import nkUtilities.plot1D as pl1
    fig  = pl1.plot1D( pngFile="f1d.png" )
    ret  = LinearFilter1D( Data=ya, alpha=0.0 )
    fig.add__plot( xAxis=xa, yAxis=ret, label=r"$\alpha=0$" )
    ret  = LinearFilter1D( Data=ya, alpha=0.2 )
    fig.add__plot( xAxis=xa, yAxis=ret, label=r"$\alpha=0.2$" )
    ret  = LinearFilter1D( Data=ya, alpha=0.5 )
    fig.add__plot( xAxis=xa, yAxis=ret, label=r"$\alpha=0.5$" )
    ret  = LinearFilter1D( Data=ya, alpha=0.5, nFilter=10 )
    fig.add__plot( xAxis=xa, yAxis=ret, label=r"$\alpha=0.5\times10$" )
    fig.set__axis()
    fig.add__legend()
    fig.save__figure()

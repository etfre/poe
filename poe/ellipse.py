import numpy
from matplotlib.patches import Ellipse

def fitEllipse(cont,method):

    x=cont[:,0]
    y=cont[:,1]

    x=x[:,None]
    y=y[:,None]

    D=numpy.hstack([x*x,x*y,y*y,x,y,numpy.ones(x.shape)])
    S=numpy.dot(D.T,D)
    C=numpy.zeros([6,6])
    C[0,2]=C[2,0]=2
    C[1,1]=-1
    E,V=numpy.linalg.eig(numpy.dot(numpy.linalg.inv(S),C))

    if method==1:
        n=numpy.argmax(numpy.abs(E))
    else:
        n=numpy.argmax(E)
    a=V[:,n]

    #-------------------Fit ellipse-------------------
    b,c,d,f,g,a=a[1]/2., a[2], a[3]/2., a[4]/2., a[5], a[0]
    num=b*b-a*c
    cx=(c*d-b*f)/num
    cy=(a*f-b*d)/num

    angle=0.5*numpy.arctan(2*b/(a-c))*180/numpy.pi
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*numpy.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*numpy.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    a=numpy.sqrt(abs(up/down1))
    b=numpy.sqrt(abs(up/down2))

    #---------------------Get path---------------------
    ell=Ellipse((cx,cy),a*2.,b*2.,angle)
    ell_coord=ell.get_verts()

    params=[cx,cy,a,b,angle]

    return params,ell_coord

def plotConts(contour_list):
    '''Plot a list of contours'''
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax2=fig.add_subplot(111)
    for ii,cii in enumerate(contour_list):
        x=cii[:,0]
        y=cii[:,1]
        ax2.plot(x,y,'-')
    plt.show(block=False)
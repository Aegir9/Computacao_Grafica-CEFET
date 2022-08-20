from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = b'\033'

# Number of the glut window.
window = 0

# Rotations for cube. 
xrot = yrot = zrot = 0.1
dx = 0
dy = 0
dz = 0

def LoadTextures():
    global texture
    texture = [ glGenTextures(1) ]

    glBindTexture(GL_TEXTURE_2D, texture[0])
    reader = png.Reader(filename='dado.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

def InitGL(Width, Height):             
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glShadeModel(GL_SMOOTH)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
    if Height == 0:                        
        Height = 1
    glViewport(0, 0, Width, Height)      
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
    global xrot, yrot, zrot, texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0.5,0.5,0.5,1.0)            
    glTranslatef(0.0,0.0,-5.0)
    glRotatef(xrot,1.0,0.0,0.0)          
    glRotatef(yrot,0.0,1.0,0.0)           
    glRotatef(zrot,0.0,0.0,1.0) 
    
    glBindTexture(GL_TEXTURE_2D, texture[0])
    glBegin(GL_QUADS)              
    
    # 1 Front Face
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    
    glTexCoord2f(0.0, 1/2); glVertex3f( 1.0, -1.0,  1.0)   
    glTexCoord2f(1/3, 1/2); glVertex3f( 1.0,  1.0,  1.0)   
    glTexCoord2f(1/3, 0.0); glVertex3f(-1.0,  1.0,  1.0)  

    # 6 Back Face
    glTexCoord2f(2/3, 1/2); glVertex3f(-1.0, -1.0, -1.0)    
    glTexCoord2f(2/3, 1.0); glVertex3f(-1.0,  1.0, -1.0)    
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    
    glTexCoord2f(1.0, 1/2); glVertex3f( 1.0, -1.0, -1.0)   
    
    # 2 Top Face
    glTexCoord2f(1/3, 0.0); glVertex3f(-1.0,  1.0, -1.0)   
    glTexCoord2f(1/3, 1/2); glVertex3f(-1.0,  1.0,  1.0)    
    glTexCoord2f(2/3, 1/2); glVertex3f( 1.0,  1.0,  1.0)    
    glTexCoord2f(2/3, 0.0); glVertex3f( 1.0,  1.0, -1.0)   

    # 5 Bottom Face       
    glTexCoord2f(1/3, 1/2); glVertex3f(-1.0, -1.0, -1.0)   
    glTexCoord2f(1/3, 1.0); glVertex3f( 1.0, -1.0, -1.0)   
    glTexCoord2f(2/3, 1.0); glVertex3f( 1.0, -1.0,  1.0)   
    glTexCoord2f(2/3, 1/2); glVertex3f(-1.0, -1.0,  1.0)    
    
    # 3 Right face
    glTexCoord2f(2/3, 0.0); glVertex3f( 1.0, -1.0, -1.0)    
    glTexCoord2f(2/3, 1/2); glVertex3f( 1.0,  1.0, -1.0)   
    glTexCoord2f(1.0, 1/2); glVertex3f( 1.0,  1.0,  1.0)    
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)  
    
    # 4 Left Face
    glTexCoord2f(0.0, 1/2); glVertex3f(-1.0, -1.0, -1.0)  
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, -1.0,  1.0)    
    glTexCoord2f(1/3, 1.0); glVertex3f(-1.0,  1.0,  1.0)   
    glTexCoord2f(1/3, 1/2); glVertex3f(-1.0,  1.0, -1.0)   
    
    glEnd()                # Done Drawing The Cube
    
    xrot = xrot + dx                 # X rotation
    yrot = yrot + dy                 # Y rotation
    zrot = zrot + dz                 # Z rotation

    glutSwapBuffers()


def keyPressed(tecla, x, y):
    global dx, dy, dz
    if tecla == ESCAPE:
        glutLeaveMainLoop()
    elif tecla == b'x' or tecla == b'X':
        dx = 0.01
        dy = 0
        dz = 0   
    elif tecla == b'y' or tecla == b'Y':
        dx = 0
        dy = 0.01
        dz = 0   
    elif tecla == b'z' or tecla == b'Z':
        dx = 0
        dy = 0
        dz = 0.01

def teclaDeRotacao(tecla, x, y):
    global xrot, yrot, zrot, dx, dy, dz
    if tecla == GLUT_KEY_LEFT:
        dx = -0                 
        dy = -0.01              
        dz = -0                     
    elif tecla == GLUT_KEY_RIGHT:
        dx = 0              
        dy = 0.01            
        dz = 0                 
    elif tecla == GLUT_KEY_UP:
        dx = 0.01              
        dy = 0           
        dz = 0       
    elif tecla == GLUT_KEY_DOWN:
        dx = -0.01               
        dy = -0         
        dz = -0       

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Dado")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(teclaDeRotacao)
    InitGL(640, 480)
    glutMainLoop()

main()

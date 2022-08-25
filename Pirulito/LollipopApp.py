from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math

class LollipopApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Dotted Lollipop")
        self.size(1100,800)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("WhiteDotsPipeline")
        GL.glUseProgram(self.pipeline)
        self.a = 0
        self.lollipopArrayBufferId = None

    def drawLollipop(self):
        n = 30
        qtdArosDoCilindro = int(n)
        tamanhoCilindro = 2
        distanciaDosAros = tamanhoCilindro/qtdArosDoCilindro
        raioCilindro = math.pi/n
        
        countDrawArrays = n*n + n*qtdArosDoCilindro

        if self.lollipopArrayBufferId == None:
            position = array('f')

            for i in range(0,n):
                theta = i*2*math.pi/n
                y = -1

                # Desenha a esfera
                for j in range(0,n):
                    phi = j*math.pi/n-math.pi/2
                    position.append(math.cos(theta)*math.cos(phi))
                    position.append(math.sin(phi))
                    position.append(math.sin(theta)*math.cos(phi))
            
                # Desenha o cilindro 
                for k in range(0, qtdArosDoCilindro):
                    y -= distanciaDosAros
                    position.append(math.cos(theta) * raioCilindro)
                    position.append(y)
                    position.append(math.sin(theta) * raioCilindro)



            self.lollipopArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.lollipopArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        GL.glBindVertexArray(self.lollipopArrayBufferId)
        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,5),glm.vec3(0),glm.vec3(0,1,0))
        model = glm.rotate(self.a,glm.vec3(0,0,1)) * glm.rotate(self.a,glm.vec3(0,1,0)) * glm.rotate(self.a,glm.vec3(1,0,0)) 
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glDrawArrays(GL.GL_POINTS,0,countDrawArrays)
        self.a += 0.001

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        
        self.drawLollipop()

LollipopApp()

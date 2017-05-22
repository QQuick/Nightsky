shaderTypesGl = {'vertex': gl.GL_VERTEX_SHADER, 'fragment': gl.GL_FRAGMENT_SHADER}

typesGen = {'coordinate': 'float32', 'colorComponent': 'float32', 'index': 'uint16'}
typesNp = {'float32': numpy.float32, 'uint16': numpy.uint16}
typesGl = {'float32': gl.GL_FLOAT, 'uint16': gl.GL_UNSIGNED_SHORT}

class Shader:
	def __init__ (self, aType, code):		
		self.shaderGl = gl.glCreateShader (shaderTypesGl [aType])
		gl.glShaderSource (self.shaderGl, code)
		gl.glCompileShader (self.shaderGl)
		
class Canvas:
    def __init__ (self, parentId, *shaders):
        parent = document.getElementById (self.parentId)
        self.createCanvas ()
        self.prepareContext ()
        self.linkShaders ()
    
    def _createCanvas (self):
        self.canvas = document.createElement ('canvas')
        self.parent.appendChild (self.canvas)
        
        self.canvas.style.width = '100%'                # Make canvas fit parent
        self.canvas.style.height = '100%'
        
        self.canvas.width  = self.canvas.offsetWidth    # Adapt internal width in pixels
        self.canvas.height = self.canvas.offsetHeight
        
    def _prepareContext (self):
        self.context = self.canvas.getContext ('webgl2')
        self.context.clearColor (0, 0, 0, 1)
        self.context.viewport (0, 0, self.canvas.width, self.canvas.height)
        self.context.js_clear (self.context.COLOR_BUFFER_BIT | self.context.DEPTH_BUFFER_BIT)
        
    def _linkShaders (self):
		programGl = self.context.glCreateProgram ()
		for shader in shaders:				
			self.context.glAttachShader (programGl, shader.shaderGl)	
		self.context.glLinkProgram (programGl)
		for shader in shaders:
			self.context.glDetachShader (programGl, shader.shaderGl)
		self.context.glUseProgram (programGl)    
        
	def setAttributes (self, attributes):
		attributeBuffer = gl.glGenBuffers (1)	                                                # Get unused identifier
		gl.glBindBuffer (gl.GL_ARRAY_BUFFER, attributeBuffer)	                                # Allocate GPU buffer
		gl.glBufferData (gl.GL_ARRAY_BUFFER, attributes.nbytes, attributes, gl.GL_STATIC_DRAW)  # Copy data to GPU buffer 
	
		stride = attributes.dtype.itemsize	
		offset = 0
		
		for attributeName in attributes.dtype.names:
			location = gl.glGetAttribLocation (self.programGl, attributeName)	                # Get meta-info object of attribute
			attribute = attributes.dtype [attributeName]
			dimension = attribute.shape [0]
			typeGen = attribute.subdtype [0] .name
			gl.glEnableVertexAttribArray (location)	                                            # Make attribute accessible in vertex attribute array
			gl.glVertexAttribPointer (                                                          # Connect vertex attribute array to the right places the in already filled buffer
                location, dimension, typesGl [typeGen],False, stride, ctypes.c_void_p (offset)
            )
			offset += attribute.itemsize
	
	def setIndices (self, indices):
		indexBuffer = gl.glGenBuffers (1)	                                                        # Get empty buffer
		gl.glBindBuffer (gl.GL_ELEMENT_ARRAY_BUFFER, indexBuffer)	                                # Make buffer current
		gl.glBufferData (gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)    # Copy data to buffer
		
	def setUniform (self, name, value):
		location = gl.glGetUniformLocation (self.programGl, name)                   # Reference to named field in program
		if isinstance (value, numpy.matrix):
			if value.shape == (4, 4):
				gl.glUniformMatrix4fv (location, 1, gl.GL_FALSE, value.T.tolist ())
			elif value.shape == (4, 1):
				gl.glUniform4fv (location, 1, value.tolist ())
			else:
				raise Exception ('Invalid uniform shape')
		elif isinstance (value, float):
			gl.glUniform1f (location, value)
		elif isinstance (value, int):
				gl.glUniform1i (location, value)
		else:
			raise Exception ('Invalid uniform type')



        
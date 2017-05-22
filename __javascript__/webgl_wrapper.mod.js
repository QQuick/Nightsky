	__nest__ (
		__all__,
		'webgl_wrapper', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var Canvas = __class__ ('Canvas', [object], {
						get __init__ () {return __get__ (this, function (self, parentId) {
							self.parentId = parentId;
							self.parent = document.getElementById (self.parentId);
							self.canvas = document.createElement ('canvas');
							self.parent.appendChild (self.canvas);
							self.canvas.style.width = '100%';
							self.canvas.style.height = '100%';
							self.canvas.width = self.canvas.offsetWidth;
							self.canvas.height = self.canvas.offsetHeight;
							self.context = self.canvas.getContext ('webgl2');
							self.context.clearColor (0, 0, 0, 1);
							self.context.viewport (0, 0, self.canvas.width, self.canvas.height);
							self.context.clear (self.context.COLOR_BUFFER_BIT | self.context.DEPTH_BUFFER_BIT);
						});},
						get drawTestImage () {return __get__ (this, function (self) {
							// pass;
						});}
					});
					__pragma__ ('<all>')
						__all__.Canvas = Canvas;
					__pragma__ ('</all>')
				}
			}
		}
	);

	(function () {
		var ww =  __init__ (__world__.webgl_wrapper);
		var canvas = null;
		var run = function (parentId) {
			canvas = ww.Canvas (parentId);
		};
		__pragma__ ('<use>' +
			'webgl_wrapper' +
		'</use>')
		__pragma__ ('<all>')
			__all__.canvas = canvas;
			__all__.run = run;
		__pragma__ ('</all>')
	}) ();

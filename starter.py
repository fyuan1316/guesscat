from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from server import app
from tornado.options import define, options


define("port", default="5000", help="port listen on")
define('debug_mode', default=True, help="is debug mode")
define('grpc_server', default='150.109.69.83', help='grpc host ip')
define('grpc_port', default='31092', help='grpc port')
define('grpc_timeout', default=60.0, help='grpc timeout float32')

define('img_height', default=224, help='image height')
define('img_width', default=224, help='image height')
define('input_mean', default=128, help='image mean')
define('input_std', default=128, help='image mean')
define('model_name', default='cat-prediction', help='model name')
define('model_signature_name', default='predict_images', help='model signature name')


if __name__ == '__main__':
    options.parse_command_line()
    app.config['DEBUG'] = options.debug_mode

    app.config['grpc_server'] = options.grpc_server
    app.config['grpc_port'] = options.grpc_port
    app.config['grpc_timeout'] = options.grpc_timeout

    app.config['img_height'] = options.img_height
    app.config['img_width'] = options.img_width
    app.config['input_mean'] = options.input_mean
    app.config['input_std'] = options.input_std

    app.config['model_name'] = options.model_name
    app.config['model_signature_name'] = options.model_signature_name

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(options.port)
    print("server listen on %s" % options.port)
    IOLoop.instance().start()

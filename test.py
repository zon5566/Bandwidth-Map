import matlab.engine

eng = matlab.engine.start_matlab()

data = eng.linspace(1,34.0,34)

eng.figure(nargout=0)
eng.hold("on", nargout=0)
eng.box("on", nargout=0)

eng.scatter(data,10,'red')
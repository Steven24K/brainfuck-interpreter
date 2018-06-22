# brainfuck-interpreter

This a little brainfuck interpreter made in Python, to run this example make sure Python 3.x is installed. 

Than simply run: (This runs the default hello world program from examples/hello.bf)

`python brainfuck.py`

To run your own BF programs run: 

`python brainfuck.py --program <PATH TO FILE>`

To see the memory state on the console run: 

`python brainfuck.py --program <PATH TO FILE> --debug True --timeout <SECCONDS>`

The timeout is optional, just to slow things down so you can easily read step by step
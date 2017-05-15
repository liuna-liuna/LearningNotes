#include <Python.h>
#include <string.h>

// function definition
static PyObject * message(PyObject *self, PyObject *args)
{
    char *fromPython, result[1024];
    if (! PyArg_Parse(args, "(s)", &fromPython))
        return NULL;
    else {
        strcpy(result, "hello, ");
        strcat(result, fromPython);
        return Py_BuildValue("s", result);
    }
}

// method registration
static PyMethodDef hello_methods[] = {
    {"message", message, METH_VARARGS, "function doc"},
    {NULL, NULL, 0, NULL}
};

/* for Python 3.4
// module definition
static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT,
    "hello",
    "module doc",
    -1,
    hello_methods
}; 
*/

// module initialization
void inithello(void) {
/* for Python 3.4
extern "C" void PyMODINIT_FUNC PyInit_hello(void) {
    return PyModule_Create(&hellomodule);
*/
	(void) Py_InitModule("hello", hello_methods);
}



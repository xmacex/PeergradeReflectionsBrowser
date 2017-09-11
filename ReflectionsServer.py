import http.server
import urllib.parse
import json
import lxml.html
import zipfile
import logging

class Reflection:
    reflectionLogger = logging.getLogger('reflectionLogger')
    reflectionLogger.setLevel(logging.INFO)
    _html = None
    _content = None

    def __init__(self, string):
        self._html = lxml.html.document_fromstring(string)
        self._content = self.createContent(self._html)

    def __str__(self):
        return lxml.html.tostring(self._content, pretty_print=True, encoding="unicode")

    def createContent(self, content):
        e = lxml.html.Element("div")
        e.classes.add("reflection")
        e.attrib['id'] = self.student()
        for he in content.body:
            e.append(he)
        return e

    def htmldoc(self):
        return lxml.html.tostring(self._html, pretty_print=True, include_meta_content_type=False)

    def student(self):
        return self._html.head.find('title').text.lstrip('Hand-in by ')

    def body(self):
        return self._html.body


class Reflections:
    reflectionsLogger = logging.getLogger('reflectionsLogger')
    reflectionsLogger.setLevel(logging.INFO)
    
    filenames = []
    storage = dict()
    
    def __init__(self, filenames):
        self.filenames = filenames
        for filename in filenames:
            self.storage[filename.rstrip(".zip")] = self.readZip(filename)
        self.reflectionsLogger.debug(self.storage)

    def readZip(self, filename):
        s = dict()
        with zipfile.ZipFile(filename) as zf:
            for name in zf.namelist():
                with zf.open(name) as file:
                    s[name.rstrip(".html")] = Reflection(file.read().decode('utf-8'))

        return s
        
    def listAssignments(self):
        return list(self.storage.keys())

    def listStudents(self, assignment):
        return list(self.storage[assignment].keys())
                        
    def getStudent(self, assignment, student):
        self.reflectionsLogger.info("Retrieving {}".format(student))
        return self.storage[assignment][student]

class ReflectionsHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    httpServerLogger = logging.getLogger('httpServerLogger')
    httpServerLogger.setLevel(logging.INFO)

    reflections = Reflections(["reflections-week2.zip", "reflections-week3.zip"])

    def passfile(self, filename):
        with open(filename) as fd:
            return "".join(fd.readlines())

    def do_GET(self):
        self.httpServerLogger.info("Serving {}".format(self.path))
        parsed_path = urllib.parse.urlparse(self.path)
        queryparams = urllib.parse.parse_qs(parsed_path.query)

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            # self.wfile.write(bytes("HTML document here", "utf-8"))
            self.wfile.write(bytes(self.passfile("ReflectionsClient.html"), "utf-8"))

        if parsed_path.path == '/ReflectionsClient.css':
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")

            self.wfile.write(bytes(self.passfile("ReflectionsClient.css"), "utf-8"))

        if parsed_path.path == '/ReflectionsClient.js':
            self.send_response(200)
            self.send_header("Content-Type", "application/js")
            self.end_headers()

            self.wfile.write(bytes(self.passfile("ReflectionsClient.js"), "utf-8"))

        if parsed_path.path == '/listassignments':
            self.httpServerLogger.info("Listing assignments")
            assignments = self.reflections.listAssignments()

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()

            self.wfile.write(bytes(json.dumps(assignments), "utf-8"))
        
        if parsed_path.path == '/liststudents':
            assignment = queryparams['a'][0]
            self.httpServerLogger.info("Listing students")
            students = self.reflections.listStudents(assignment)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            # self.wfile.write(bytes("\n".join(students), "utf-8"))
            self.wfile.write(bytes(json.dumps(students), "utf-8"))

        elif parsed_path.path == '/student':
            assignment = queryparams['a'][0]
            studentname = queryparams['s'][0]
            
            self.httpServerLogger.info("Returning student".format(studentname))
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            self.wfile.write(bytes(str(self.reflections.getStudent(assignment, studentname)), "utf-8"))

def main():
    server = http.server.HTTPServer(('', 8000), ReflectionsHTTPRequestHandler)
    server.serve_forever()
        
if __name__ == "__main__":
    main()

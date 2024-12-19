import grpc
from concurrent import futures
import time
import glossary_pb2
import glossary_pb2_grpc
from google.protobuf.empty_pb2 import Empty

class GlossaryServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self):
        self.terms = {
            "gRPC": glossary_pb2.Term(keyword="gRPC", description="Remote Procedure Call framework by Google"),
            "Docker": glossary_pb2.Term(keyword="Docker", description="Platform for containerization of applications"),
            "Protocol Buffers": glossary_pb2.Term(keyword="Protocol Buffers", description="Language-neutral serialization mechanism"),
            "Python": glossary_pb2.Term(keyword="Python", description="High-level programming language for various domains"),
        }

    def GetTerms(self, request, context):
        response = glossary_pb2.GetTermsResponse()
        for term in self.terms.values():
            response.terms.append(term)
        return response

    def GetTerm(self, request, context):
        term = self.terms.get(request.keyword)
        if term:
            return term
        else:
            context.set_details(f"Term '{request.keyword}' not found.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return glossary_pb2.Term()

    def AddTerm(self, request, context):
        term = glossary_pb2.Term(keyword=request.keyword, description=request.description)
        self.terms[request.keyword] = term
        return term

    def UpdateTerm(self, request, context):
        if request.keyword in self.terms:
            self.terms[request.keyword].description = request.description
            return self.terms[request.keyword]
        else:
            context.set_details(f"Term '{request.keyword}' not found.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return glossary_pb2.Term()

    def DeleteTerm(self, request, context):
        if request.keyword in self.terms:
            del self.terms[request.keyword]
            return Empty()
        else:
            context.set_details(f"Term '{request.keyword}' not found.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at port 50051...")
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

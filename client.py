import grpc
import glossary_pb2
import glossary_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

    print("Получение списка всех терминов:")
    terms_response = stub.GetTerms(glossary_pb2.GetTermsRequest())
    for term in terms_response.terms:
        print(f"{term.keyword}: {term.description}")
    print()

    print("Добавление нового термина:")
    add_response = stub.AddTerm(glossary_pb2.AddTermRequest(
        keyword="API", 
        description="Application Programming Interface"
    ))
    print(f"Добавлено: {add_response.keyword} - {add_response.description}\n")

    print("Получение списка всех терминов:")
    terms_response = stub.GetTerms(glossary_pb2.GetTermsRequest())
    for term in terms_response.terms:
        print(f"{term.keyword}: {term.description}")
    print()

    print("Получение информации о термине:")
    term_response = stub.GetTerm(glossary_pb2.GetTermRequest(keyword="API"))
    print(f"Термин: {term_response.keyword} - {term_response.description}\n")


    print("Обновление термина:")
    update_response = stub.UpdateTerm(glossary_pb2.UpdateTermRequest(
        keyword="API", 
        description="Updated description"
    ))
    print(f"Обновлено: {update_response.keyword} - {update_response.description}\n")

    print("Удаление термина:")
    delete_response = stub.DeleteTerm(glossary_pb2.DeleteTermRequest(keyword="API"))
    print("Термин удалён.\n")

    print("Повторное получение списка всех терминов:")
    terms_response = stub.GetTerms(glossary_pb2.GetTermsRequest())
    for term in terms_response.terms:
        print(f"{term.keyword}: {term.description}")

if __name__ == '__main__':
    run()

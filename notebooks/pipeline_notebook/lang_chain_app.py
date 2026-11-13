from flask import Flask, request, jsonify

from function import vcs, utils, build_chain

# Build the vector store, retriever, LLM and chain once at startup, not on every request
vdb = vcs()
retriever, prompt_template, llm = utils(k=5, vectorstore=vdb)
chain = build_chain(retriever, prompt_template, llm)

app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Accept either form data or a JSON body: {"question": "..."}
    data = request.get_json(silent=True) or request.form
    concept = (data.get('question') or '').strip()
    if not concept:
        return jsonify(error="Send a non-empty 'question' field."), 400

    answer = chain.invoke(concept)
    return jsonify(question=concept, answer=answer)


if __name__ == '__main__':
    app.run()

from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import bcchapi

app = Flask(__name__)
load_dotenv()

@app.route('/')
def home():
    return 'Microservicio BBCh funcionando. Usa /dolar para obtener el valor del dólar.'


@app.route('/dolar', methods=['GET'])
def obtener_valor_dolar():
    usuario = os.getenv("BCCH_USER")
    contrasena = os.getenv("BCCH_PASSWORD")

    try:
        siete = bcchapi.Siete(usuario, contrasena)
        cuadro = siete.cuadro(
            series=["F073.TCO.PRE.Z.D"],
            nombres=["dolar"],
            desde="2025-01-01",
            frecuencia="D",
            observado={"dolar": "last"}
        )

        # Tomamos el último valor disponible
        ultimo_valor = cuadro["dolar"].dropna().iloc[-1]

        return jsonify({
            "valor_dolar": float(ultimo_valor)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)

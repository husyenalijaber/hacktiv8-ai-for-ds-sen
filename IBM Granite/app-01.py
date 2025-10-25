# app-01.py
import getpass
import os
import replicate

# Minta user masukkan Replicate API Key
api_key = getpass.getpass("Masukkan REPLICATE_API_TOKEN kamu: ").strip()
os.environ["REPLICATE_API_TOKEN"] = api_key

# Model IBM Granite di Replicate (bisa diganti varian lain)
MODEL_ID = "ibm-granite/granite-3.1-8b-instruct"

print("\n=== ChatBot IBM Granite (via Replicate) ===")
print("Ketik 'exit' untuk keluar.\n")

chat_history = []

while True:
    prompt = input("User: ").strip()
    if prompt.lower() in ["exit", "quit"]:
        print("Keluar dari chat...")
        break

    chat_history.append({"role": "user", "content": prompt})

    try:
        # Kirim ke Replicate
        response = replicate.run(
            MODEL_ID,
            input={"prompt": prompt}
        )
        # Kadang hasilnya list, kadang string
        if isinstance(response, list):
            output = "".join(response)
        else:
            output = str(response)
    except Exception as e:
        output = f"[Error] Gagal memanggil model: {e}"

    print("AI:", output, "\n")
    chat_history.append({"role": "assistant", "content": output})

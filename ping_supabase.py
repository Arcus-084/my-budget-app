import os 
from supabase import create_client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def keep_alive() :
    try :
        supabase = create_client(url, key)
        supabase.table('transaksi').select('id').limit(1).execute()
        print("✅ Sinyal Berhasil Dikirim!")
    except Exception as e :
        print(f"❌ Error: {e}")
if __name__ == "__main__":
    keep_alive()
    
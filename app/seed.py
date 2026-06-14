import qrcode
from sqlmodel import Session, select
from pathlib import Path

from app.database import engine
from app.models import EsimProfile

def generate_qr_code(qr_code_value, temp_number):
    img = qrcode.make(qr_code_value)
    # type(img)

    # Walidacaj istnienia folderu i ewentualne jego utworzenie
    folder_path = Path("static/qrcodes")
    if not folder_path.exists():
        folder_path.mkdir(parents=True)

    img.save("static/qrcodes/example_file_" + str(temp_number)+ ".png")
    return "/static/qrcodes/example_file_"+str(temp_number)+".png"

def seed_5_example_profiles():
    temp_number = 0
    with Session(engine) as session:
        for i in range(5):

            qr_code_value_temp = "Profile" + str(temp_number)  

            querry = select(EsimProfile).where(EsimProfile.qr_code_value == qr_code_value_temp)
            
            while session.exec(querry).first():
                temp_number += 1
                qr_code_value_temp = "Profile" + str(temp_number)
                querry = select(EsimProfile).where(EsimProfile.qr_code_value == qr_code_value_temp) 

            session.add(
                EsimProfile(qr_code_value = qr_code_value_temp, qr_image_url = (generate_qr_code(qr_code_value_temp, temp_number)))
            )
            temp_number += 1
        session.commit()

if __name__ == "__main__":
    print("Starting seed...")
    seed_5_example_profiles()
    print("Seed completed")
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from utils.database import Base

# Database Model


class UploadedImage(Base):
    __tablename__ = 'uploaded_images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    upload_time = Column(DateTime, nullable=False)
    image_name = Column(String, nullable=False)
    status = Column(String,  nullable=False)

    def __repr__(self):
        return f"UploadedImage(id={self.id}, upload_time={self.upload_time}, image_name={self.image_name}, " \
               f"image_size={self.image_size}, is_large={self.is_large})"

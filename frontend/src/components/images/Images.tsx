import React, { useState } from "react";
import ImageUpload from "./ImageUpload"; // Your upload component
import ImageDisplay from "./ImageDisplay"; // Your image display component

export interface CustomImageData {
  id: string;
  image: string;
}

const Images: React.FC = () => {
  // TODO: Make it so that when the user refreshes the page, it preserves the image
  const [imageData, setImageData] = useState<CustomImageData | null>(null);

  const handleImageDataChange = (data: any) => {
    setImageData(data);
  };

  return (
    <div>
      <h1>Processed Images</h1>
      <div>
        {!imageData && (
          <ImageUpload onImageDataChange={handleImageDataChange} />
        )}
      </div>
      <div>
        {imageData && (
          <ImageDisplay
            imagesData={imageData}
            onImageDataChange={handleImageDataChange}
          />
        )}
      </div>
    </div>
  );
};

export default Images;

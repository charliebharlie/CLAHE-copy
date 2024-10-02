import React, { useState, useEffect } from "react";
import { CustomImageData } from "./Images";
interface ImageDisplayProps {
  imagesData: CustomImageData | null;
  onImageDataChange: (data: any) => void;
}

const ImageDisplay: React.FC<ImageDisplayProps> = ({
  imagesData,
  onImageDataChange: setImageData,
}) => {
  const [imageNames, setImageNames] = useState<string[]>([]);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [images, setImages] = useState<Record<string, string>>({});

  useEffect(() => {
    unpackImageData();
  }, [imagesData]);

  const unpackImageData = () => {
    if (imagesData) {
      // create a hashmap of the key being the image name and the image being the value
      const imageData = Object.fromEntries(
        Object.entries(imagesData).map(([key, value]) => [key, value.image]),
      );
      console.log(imagesData);

      setSelectedImage(Object.keys(imagesData)[0]);
      setImageNames(Object.keys(imagesData));
      setImages(imageData);
    }
  };

  const clearImage = async () => {
    try {
      const response = await fetch("http://localhost:5000/clear_images", {
        method: "POST",
      });

      const data = (await response.json()) as { message: string };
      if (response.status !== 200) {
        alert(data.message);
        return;
      } else {
        setImages({});
        setImageNames([]);
        setSelectedImage(null);
        setImageData(null);
      }
    } catch (error) {
      console.error("Unable to clear images", error);
      return;
    }
  };

  return (
    <div>
      <div>
        {selectedImage && (
          <img
            src={`data:image/png;base64,${images[selectedImage]}`}
            alt={`${selectedImage}`}
          />
        )}
      </div>

      <div>
        {imageNames.map((name) => (
          <button key={name} onClick={() => setSelectedImage(name)}>
            {name}
          </button>
        ))}
        {imageNames.length > 0 && (
          <button onClick={() => clearImage()}>Clear Images</button>
        )}
      </div>
    </div>
  );
};

export default ImageDisplay;

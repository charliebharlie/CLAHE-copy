import React, { useState, ChangeEvent, useEffect, useRef } from "react";
import { CustomImageData } from "./Images";
interface ImageUploadProps {
  onImageDataChange: (data: any) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({
  onImageDataChange: setImageChange,
}) => {
  const imageFile = useRef<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  // Check if the session storage already has an image or not
  useEffect(() => {
    const file = sessionStorage.getItem("image_file");
    const preview = sessionStorage.getItem("image_preview");
    if (file && preview) {
      imageFile.current = JSON.parse(file);
      setImagePreview(JSON.parse(preview));
    }
  }, []);

  // Update the session storage whenever the selected image changes
  useEffect(() => {
    console.log(JSON.stringify(imageFile));
    console.log(JSON.stringify(imagePreview));
    if (imageFile && imagePreview) {
      sessionStorage.setItem("image_file", JSON.stringify(imageFile));
      sessionStorage.setItem("image_preview", JSON.stringify(imagePreview));
      // console.log(selectedImage.propertyIsEnumerable("name"));
    }
  }, [imageFile]);

  const handleFetchImages = async () => {
    try {
      // TODO: Need to be able to handle png's and also come up with a way to make the algorithm faster on large images
      const response = await fetch("http://localhost:5000/get_image_data");

      if (response.status !== 200) {
        console.log("No images to display");
        return;
      }

      const data: Record<string, CustomImageData> = await response.json();

      if (!data || Object.keys(data).length === 0) {
        console.log("Error fetching images");
        return;
      } else {
        return data;
      }
    } catch (error) {
      console.error("Error fetching image:", error);
      return;
    }
  };

  const handleUpload = async () => {
    if (!imageFile) return;

    const formData = new FormData();
    formData.append("file", imageFile);

    try {
      // console.log("FormData contents:", formData.get("file"));
      const response = await fetch("http://localhost:5000/user_upload_image", {
        method: "POST",
        body: formData,
        headers: {},
      });

      if (response.ok) {
        const data = await handleFetchImages();
        setImageChange(data);
        console.log("Upload successful:", data);
      } else {
        console.error("Upload failed:", response.statusText);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleFileSeclection = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith("image/")) {
      imageFile.current = file;
      console.log(URL.createObjectURL(file));
      setImagePreview(URL.createObjectURL(file)); // Preview the image
    } else {
      // TODO: Set this image to blank, but setting state doesn't update until next render
      setImagePreview(null);
      imageFile.current = null;

      event.target.value = "";
      alert("Please select a valid image file.");
    }
  };

  return (
    <div>
      {/* Image Preview */}
      <div>
        {imagePreview && (
          <img src={imagePreview} alt="Preview" style={{ width: "200px" }} />
        )}
      </div>

      {/* Image selection and upload  */}
      <div>
        <input type="file" accept="image/*" onChange={handleFileSeclection} />
        <button onClick={handleUpload} disabled={!imageFile}>
          Upload Image
        </button>
      </div>
    </div>
  );
};

export default ImageUpload;

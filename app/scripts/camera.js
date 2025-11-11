let track;
let imageCapture;

export async function videoCapture() {
  try {
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });
    track = mediaStream.getVideoTracks()[0];
    imageCapture = new ImageCapture(track);
    // console.log("Photo capabilities: ", imageCapture.getPhotoCapabilities());
    return true;
  } catch (err) {
    console.error("Failed to access webcam:", err);
    return false;
  }
}

export async function getFrame() {
  try {
    const bitmap = await imageCapture.grabFrame();
    const img = await imageBitmapToImage(bitmap);
    return img;
  } catch (err) {
    console.error("Failed to capture frame:", err);
  }
}

async function imageBitmapToImage(bitmap) {
  const canvas = document.createElement("canvas");
  canvas.width = bitmap.width;
  canvas.height = bitmap.height;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(bitmap, 0, 0);
  const img = new Image();
  img.src = canvas.toDataURL("image/png");
  await new Promise((resolve) => (img.onload = resolve));
  return img;
}

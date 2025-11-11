import { videoCapture, getFrame } from "./camera.js";
import { inference } from "./yolo.js";

async function main() {
  const ready = await videoCapture();

  if (!ready) return;

  async function loop() {
    const frame = await getFrame();
    await inference(frame);
    requestAnimationFrame(loop);
  }

  loop();
}

main();

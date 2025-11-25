import { CameraParams } from "@/types/camera";
import api from "@/api/api";

export async function getCameras() {
  try {
    const { data } = await api.get<CameraParams[]>("/cameras");
    return data;
  } catch (error: any) {
    console.debug("API error:", error.message || error);
    throw error;
  }
}

export interface CameraParams {
  id: number;
  name: string;
  ip_address: string;
  is_online: boolean;
  location?: string | null;
}

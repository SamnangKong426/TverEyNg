"use client";

import { useEffect, useState } from "react";
import { AppSidebar } from "@/components/app-sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { getCameras } from "@/services/camera";
import type { CameraParams } from "@/types/camera";

export default function Page() {
  const [cameras, setCameras] = useState<CameraParams[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchCameras() {
      try {
        const data = await getCameras();
        setCameras(data);
      } catch (err) {
        console.error("Failed to fetch cameras:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchCameras();
  }, []);

  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "350px",
        } as React.CSSProperties
      }
    >
      <AppSidebar />
      <SidebarInset>
        <header className="bg-background sticky top-0 flex shrink-0 items-center gap-2 border-b p-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-[orientation=vertical]:h-4"
          />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Security Camera</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          {loading ? (
            <p>Loading cameras...</p>
          ) : (
            <div className="grid auto-rows-min gap-4 xl:grid-cols-2">
              {cameras.map((cam) => (
                <iframe
                  key={cam.id}
                  src={cam.ip_address}
                  width="800"
                  height="600"
                  className="bg-muted/50 aspect-video rounded-xl"
                  title={cam.name}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  referrerPolicy="strict-origin-when-cross-origin"
                  allowFullScreen
                ></iframe>
              ))}
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}

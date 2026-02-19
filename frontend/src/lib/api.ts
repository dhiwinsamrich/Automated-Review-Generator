// Mock API service for development
// Switch to real endpoints by changing USE_MOCK to false

const USE_MOCK = false;
const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export interface ReviewData {
  client_name: string;
  business_name: string;
  draft_text: string;
  rating: number;
  gbp_review_url: string;
  status: "pending" | "copied" | "declined" | "expired";
  regeneration_count: number;
  max_regenerations: number;
}

const mockReview: ReviewData = {
  client_name: "Sarah",
  business_name: "Lumix Digital Studio",
  draft_text:
    "I had an exceptional experience working with Lumix Digital Studio. From the initial consultation to the final delivery, the team demonstrated outstanding professionalism and creativity. They truly understood my vision and brought it to life in ways I hadn't even imagined. The attention to detail was remarkable, and the communication throughout the project was seamless. I would highly recommend them to anyone looking for top-tier digital solutions.",
  rating: 5,
  gbp_review_url: "https://g.page/review/example",
  status: "pending",
  regeneration_count: 0,
  max_regenerations: 3,
};

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

export async function fetchReview(token: string): Promise<ReviewData> {
  if (USE_MOCK) {
    await delay(1200);
    if (token === "expired") throw { status: 410, message: "Link has expired" };
    if (token === "error") throw { status: 500, message: "Server error" };
    return { ...mockReview };
  }

  const res = await fetch(`${API_BASE}/review/${token}`, {
    headers: { "ngrok-skip-browser-warning": "true" },
  });
  if (!res.ok) {
    throw { status: res.status, message: await res.text() };
  }
  return res.json();
}

export async function markCopied(token: string): Promise<void> {
  if (USE_MOCK) {
    await delay(400);
    return;
  }

  const res = await fetch(`${API_BASE}/review/${token}/copied`, {
    method: "POST",
    headers: { "ngrok-skip-browser-warning": "true" },
  });
  if (!res.ok) throw { status: res.status, message: await res.text() };
}

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getIronSession } from "iron-session";
import { sessionOptions, SessionData } from "@/lib/session";

export async function proxy(request: NextRequest) {
  // Create a minimal cookie store (read-only) for the proxy
  const cookieStore = {
    get: (name: string) => {
      const cookie = request.cookies.get(name);
      if (cookie) {
        return { name: cookie.name, value: cookie.value };
      }
      return undefined;
    },
    set: () => {}, // dummy – we never save the session in the proxy
  };

  const session = await getIronSession<SessionData>(cookieStore, sessionOptions);
  const { pathname } = request.nextUrl;

  // Allow login page and static assets
  if (
    pathname === "/admin/login" ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api")
  ) {
    return NextResponse.next();
  }

  // Protect /admin/* routes
  if (pathname.startsWith("/admin")) {
    if (!session.isLoggedIn) {
      return NextResponse.redirect(new URL("/admin/login", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*"],
};
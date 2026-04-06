import { describe, expect, it } from "vitest";

import { buildApiUrl } from "./api";


describe("buildApiUrl", () => {
  it("returns relative path when base is empty", () => {
    expect(buildApiUrl("/api/v1/chat", "")).toBe("/api/v1/chat");
  });

  it("returns relative path when base is slash", () => {
    expect(buildApiUrl("api/v1/chat", "/")).toBe("/api/v1/chat");
  });

  it("joins full base URL without duplicate slash", () => {
    expect(buildApiUrl("/api/v1/chat", "https://example.app")).toBe(
      "https://example.app/api/v1/chat"
    );
  });

  it("trims trailing slash from base URL", () => {
    expect(buildApiUrl("api/v1/evaluation/summary", "https://example.app/")).toBe(
      "https://example.app/api/v1/evaluation/summary"
    );
  });
});

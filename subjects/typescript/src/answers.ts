function normalizeTitle(value: unknown): string | undefined {
  if (typeof value === "string") {
    return value.trim();
  } else {
    return undefined;
  }
}

type Result =
  | { ok: true; title: string }
  | { ok: false; error: string };

function getMessage(result: Result): string {
  if (result.ok) {
    return result.title;
  } else {
    return result.error;
  }
}

function readTitle(value: unknown): string | undefined {
  if (value !== null && typeof value === "object"
    && "title" in value && typeof value.title === "string") {
    return value.title;
  }
  return undefined;
}

type Task = {
  id: number,
  title: string,
  completed: boolean,
  description?: string
}

function getDescription(task: Task): string | undefined {
  if (task.description !== undefined) {
    return task.description;
  }
}

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

function firstItem1(value: unknown) {
    return value.slice(0, 1);
}

function firstItem(value: unknown): unknown[] | undefined {
  if (Array.isArray(value)) {
    return value.slice(0, 1);
  }
}

import { EventEmitter } from "events";

interface Settings {
  theme: string;
  fontSize: number;
  language: string;
}

const settings: Settings = { theme: "dark", fontSize: 14, language: "en" };

export function getSetting(name: string) {
  return settings[name];
}

export function settingNames<T>(obj: T): string[] {
  const names: string[] = [];
  for (const key in obj) {
    const name: keyof T = key;
    names.push(name);
  }
  return names;
}

function logged(target: any, key: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`${key}(${args.join(", ")})`);
    return original.apply(this, args);
  };
  return descriptor;
}

export class SettingsStore extends EventEmitter {
  private values: { [key: string]: unknown } = { ...settings };

  @logged
  set(name: string, value: unknown) {
    this.values[name] = value;
    this.emit("change", name, value);
  }

  get(name: string) {
    return this.values[name];
  }
}

const store = new SettingsStore();
store.on("change", (name: string) => console.log(`changed: ${name}`));
store.set("theme", "light");
console.log(getSetting("fontSize"), settingNames(settings));

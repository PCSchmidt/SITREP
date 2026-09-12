export interface Briefing {
  id: string;
  /** True when this copy came from the on-device cache after a failed fetch. */
  isStale?: boolean;
  /** When this copy was last written to the cache. */
  cachedAt?: string;
  timestamp: string;
  title: string;
  preview: string;
  regions: string[];
  bluf: string;
  readTime: number;
  content: {
    region: string;
    bluf: string;
    sections: {
      title: string;
      content: string;
    }[];
  }[];
  sources: {
    title: string;
    publication: string;
    date: string;
    url: string;
  }[];
}

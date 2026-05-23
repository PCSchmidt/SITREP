export interface Briefing {
  id: string;
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

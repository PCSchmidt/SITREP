import { Briefing } from '../types/briefing';

export const mockBriefings: Briefing[] = [
  {
    id: '2026-05-22',
    timestamp: '2026-05-22 0600 UTC',
    title: 'Global Security Update',
    preview: 'Tensions escalate in Middle East following diplomatic breakdown. Regional analysis shows increased military positioning across Indo-Pacific theater.',
    regions: ['M.EAST', 'INDO-PAC', 'EUR'],
    bluf: 'U.S.-Israel military cooperation intensifies amid regional tensions. Economic blockades affect global supply chains. Naval deployments increase in contested waters.',
    readTime: 8,
    content: [
      {
        region: 'Middle East',
        bluf: 'The U.S.-Israel strategic partnership strengthens as regional actors reposition forces.',
        sections: [
          {
            title: 'Covert Operations',
            content: 'Intelligence indicates coordinated activities targeting key infrastructure. Multiple state actors involved in counter-operations.',
          },
          {
            title: 'Military Operations',
            content: 'U.S. aircraft deployments to regional bases increase. Allied forces conduct joint exercises in strategic corridors.',
          },
        ],
      },
      {
        region: 'Indo-Pacific',
        bluf: 'Naval activity in contested waters reaches multi-year highs.',
        sections: [
          {
            title: 'Naval Deployments',
            content: 'Carrier strike groups reposition throughout theater. Freedom of navigation operations continue at steady pace.',
          },
        ],
      },
      {
        region: 'Europe and Africa',
        bluf: 'NATO exercises expand scope amid evolving threat landscape.',
        sections: [
          {
            title: 'Alliance Coordination',
            content: 'Multinational exercises focus on rapid response capabilities. Interoperability improvements noted across participating forces.',
          },
        ],
      },
    ],
    sources: [
      {
        title: 'Congressional Report Reveals Classified Operations',
        publication: 'THE AVIATIONIST',
        date: '2026-05-21',
        url: 'https://example.com',
      },
      {
        title: 'CENTCOM Head Calls for Increased Regional Presence',
        publication: 'DEFENSE ONE',
        date: '2026-05-20',
        url: 'https://example.com',
      },
      {
        title: 'Naval Tensions Rise in Disputed Waters',
        publication: 'REUTERS',
        date: '2026-05-20',
        url: 'https://example.com',
      },
    ],
  },
  {
    id: '2026-05-15',
    timestamp: '2026-05-15 0600 UTC',
    title: 'Weekly Intelligence Briefing',
    preview: 'Strategic positioning continues across multiple theaters. Diplomatic engagements show mixed results.',
    regions: ['W.HEM', 'EUR'],
    bluf: 'Western Hemisphere partnerships strengthen. European defense posture adjusts to emerging challenges.',
    readTime: 6,
    content: [],
    sources: [],
  },
];

import { useNavigate } from 'react-router-dom';

const faqItems = [
  {
    question: 'How do I register to vote?',
    answer: 'Registration rules vary by jurisdiction, but most voters need to confirm their eligibility, submit an application before the registration deadline, and bring ID on election day. Ask August your specific location to get precise instructions.'
  },
  {
    question: 'What should I bring to the polling place?',
    answer: 'Bring a valid ID if required, your voter registration card if you have one, and any supporting documents requested by your local election office. Check the assistant for your local requirements.'
  },
  {
    question: 'When is election day and what happens after voting?',
    answer: 'Election day is usually set by your government. After you vote, ballots are counted and results are certified according to local timelines. Ask the assistant for your election timeline and key dates.'
  },
  {
    question: 'Can I vote early or by mail?',
    answer: 'Many places offer early voting or mail-in ballots. Eligibility and deadlines depend on your area. Use the assistant to determine your options and next steps.'
  }
];

const guidanceSections = [
  {
    title: 'How to Register',
    description: 'Learn the registration steps, required documents, and deadlines so you can become a confident voter.'
  },
  {
    title: 'How to Vote',
    description: 'Understand the election day process, from arriving at the polling place to casting your ballot safely.'
  },
  {
    title: 'Election Timeline',
    description: 'Track important milestones such as registration deadlines, early voting windows, and result announcements.'
  },
  {
    title: 'Voter Rights',
    description: 'Know your rights at the polling place and what to do if you encounter issues while voting.'
  }
];

export default function HelpPage() {
  const navigate = useNavigate();

  return (
    <div className="help-page">
      <div className="help-hero">
        <div>
          <h2>Election Learning Center</h2>
          <p>Get easy-to-follow guidance on voter registration, election timelines, and voting steps.</p>
        </div>
        <button className="btn-primary" onClick={() => navigate('/')}>Back to dashboard</button>
      </div>

      <section className="help-section">
        <h3>Structured guidance</h3>
        <div className="help-grid">
          {guidanceSections.map((section) => (
            <div key={section.title} className="help-card">
              <h4>{section.title}</h4>
              <p>{section.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="help-section">
        <div className="section-header">
          <h3>Quick FAQ for voters</h3>
        </div>
        <div className="faq-list">
          {faqItems.map((item) => (
            <div key={item.question} className="faq-item">
              <h4>{item.question}</h4>
              <p>{item.answer}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="help-section" style={{ marginTop: '1.5rem' }}>
        <h3>Need more help?</h3>
        <p>Use the chat assistant in the bottom-right corner to ask about your registration status, voting rules, deadlines, and election day steps.</p>
      </section>
    </div>
  );
}

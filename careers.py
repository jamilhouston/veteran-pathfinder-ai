"""Transparent illustrative catalog. Not a validated military crosswalk."""
def obj(properties):
    return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)
STR = {'type':'string'}
def arr(item): return {'type':'array','items':item}
SCHEMA = obj({'careers':arr(obj({'title':STR,'why':STR,'gaps':arr(STR),'next_step':STR})),
              'translations':arr(obj({'military':STR,'civilian':STR})), 'summary':STR,'bullets':arr(STR)})
CATALOG = [
 ('IT support specialist', ['cyber','network','computer','technology','signal','25b','3d'], 'troubleshooting and supporting technology users', ['Practice a documented help-desk troubleshooting workflow.','Compare your certifications with requirements in three local IT support postings.']),
 ('Logistics coordinator', ['supply','logistics','transport','inventory','92','warehouse'], 'coordinating materials, schedules and resources', ['Explore a civilian inventory or ERP tool.','Practice a spreadsheet inventory reconciliation exercise.']),
 ('Project coordinator', ['planning','project','business','operations','lead','manage'], 'organizing tasks, communicating updates and tracking delivery', ['Create a sample project schedule and risk register.','Review entry-level coordination roles before considering paid credentials.']),
 ('Maintenance technician', ['mechanic','maintenance','repair','equipment','hands-on','91'], 'inspecting equipment and resolving practical problems', ['Check industry-specific safety and licensing requirements.','Identify which tools and equipment your experience covers.']),
 ('Training coordinator', ['teach','train','people','instruct','mentor'], 'supporting learning and communicating processes', ['Build a short training outline and evaluation checklist.','Practice adapting a technical procedure for a civilian audience.']),
 ('Operations coordinator', ['process','routine','systems','data','admin'], 'documenting workflows and keeping daily activities organized', ['Practice spreadsheet reporting with a sample operations dashboard.','Compare coordination duties across three industries.'])]

def demo(p):
    text = ' '.join(p.values()).lower()
    ranked = sorted(CATALOG, key=lambda item:sum(word in text for word in item[1]), reverse=True)[:3]
    careers = []
    for title, words, bridge, gaps in ranked:
        hits = [word for word in words if word in text]
        reason = ('Your profile mentions ' + ', '.join(hits[:3]) + ', which may connect to ' + bridge + '.') if hits else ('An additional pathway to explore: ' + bridge + '. The demo has limited evidence for this suggestion.')
        reason += f" Your preference for {p['collaboration'].lower()} and {p['structure'].lower()} can guide questions about the actual workplace; it does not establish suitability."
        careers.append(dict(title=title,why=reason,gaps=gaps,next_step='Review three job descriptions and mark requirements you can evidence, need to learn, or want to ask about.'))
    translations = [{'military':p['role'], 'civilian':'Describe the role through the tasks you actually performed; expand military abbreviations for civilian readers.'}]
    if p['responsibilities']:
        translations.append({'military':p['responsibilities'],'civilian':'Turn each responsibility into an action + task + verified result. Example structure: Coordinated [activity] for [team or scope], resulting in [verified outcome].'})
    mappings = [('inventory','Inventory accountability','Inventory control and reconciliation'),
                ('supply','Supply requests','Procurement and resource coordination'),
                ('train','Training team members','Employee onboarding and instruction'),
                ('network','Network support','IT infrastructure troubleshooting'),
                ('maintenance','Equipment maintenance','Preventive maintenance and technical problem-solving')]
    for term, military, civilian in mappings:
        if term in (p['role']+' '+p['responsibilities']).lower():
            translations.append({'military':military,'civilian':civilian+' — use only if this accurately describes your work.'})
    education = f" Education / credentials reported: {p['education']}." if p['education'] else ''
    return dict(careers=careers,translations=translations,
        summary=f"Military professional with {p['years']} years of experience in {p['role']}, exploring civilian opportunities in {p['interests']}."+education,
        bullets=['Performed [specific task from your role] using [tools or process]; achieved [verified result].',
                 'Collaborated with [team or stakeholders] to deliver [specific activity] within [verified timeframe].',
                 'Applied [confirmed skill] to solve [specific problem], improving [verified outcome].'])

from flask import Flask, jsonify
from flask_cors import CORS
from scrapers.bardeen import scrape_bardeen
from scrapers.n8n import scrape_n8n
from scrapers.zapier import scrape_zapier
import asyncio
import json
from dataclasses import asdict
# from database import get_workflows

app = Flask(__name__)
CORS(app)
from sqlalchemy import create_engine, Column, Integer, String, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///workflows.db')
Base.metadata.create_all(engine)

class Workflow(Base):
    __tablename__ = 'workflows'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    tags = Column(JSON)
    platform = Column(String)

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

Session = sessionmaker(bind=engine)

@app.route('/workflows', methods=['GET'])
def get_workflows_endpoint():
    session = Session()

    # Instead of using Workflow.query, use session.query(Workflow)
    workflows = session.query(Workflow).all()
    # workflows = get_workflows()
    result_dicts = [to_dict(obj) for obj in workflows]

    for d in result_dicts:
        if d['tags']:
            d['tags'] = list(d['tags'])
    print(result_dicts)
    return json.dumps(result_dicts)

if __name__ == '__main__':
    # print("Hello World")
    engine = create_engine('sqlite:///workflows.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Get playbooks from Bardeen (assuming you have a function to do this)
    playbooks = scrape_bardeen()
    # Parse the playbook data and insert into the database
    for playbook in playbooks:
        workflow = Workflow(
            name=playbook['name'],
            description=playbook['description'],
            tags=playbook['tags'],
            platform=playbook['platform'],
        )
        session.add(workflow)

    playbooks = asyncio.run(scrape_n8n())
    for playbook in playbooks:
        workflow = Workflow(
            name=playbook['name'],
            description=playbook['description'],
            tags=playbook['tags'],
            platform=playbook['platform'],
        )
        session.add(workflow)

    # playbooks = scrape_zapier()
    # for playbook in playbooks:
    #     workflow = Workflow(
    #         name=playbook['name'],
    #         description=playbook['description'],
    #         playbook_data=playbook['playbook_data']
    #     )
    #     session.add(workflow)

    # Commit the changes and close the session
    session.commit()
    session.close()
    app.run(debug=True)
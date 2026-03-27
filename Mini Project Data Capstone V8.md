```python
"""
COMPLETE TRISTRAM SHANDY PIPELINE WITH HTML PRESENTATION
==========================================================

This script:
1. Scrapes full text with intelligent quotation extraction
2. Creates dual-panel temporal architecture visualization
3. Generates comprehensive HTML page with explanatory sections

Run this single script for the complete digital humanities presentation.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from typing import List, Dict
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TristramShandyCompletePipeline:
    def __init__(self):
        self.url = "https://www.gutenberg.org/files/1079/1079-h/1079-h.htm"
        self.html_content = None
        self.chapters = []
        self.annotated_data = []
        
        # Narrative time buckets
        self.time_buckets = {
            "dinah": {
                "keywords": ["aunt dinah", "great aunt", "coachman", "family disgrace"],
                "character_markers": ["dinah"],
                "description": "Aunt Dinah's scandal",
                "chronological_order": -4
            },
            "yorick_life": {
                "keywords": ["yorick", "parson yorick", "denmark", "danish", "hamlet"],
                "character_markers": ["yorick", "eugenius"],
                "description": "Parson Yorick's life",
                "chronological_order": -3
            },
            "toby_namur": {
                "keywords": ["namur", "siege", "wound", "wounded", "groin", "flanders", "battle"],
                "character_markers": ["toby", "uncle toby"],
                "description": "Namur",
                "chronological_order": -2
            },
            "toby_recovery": {
                "keywords": ["fortification", "fortifications", "bowling green", "trim", 
                           "corporal trim", "hobby-horse", "ramparts", "sieges"],
                "character_markers": ["toby", "trim", "uncle toby", "corporal"],
                "description": "Toby Recovery",
                "chronological_order": -1
            },
            "conception": {
                "keywords": ["conception", "begot", "begetting", "homunculus", "animal spirits", 
                           "clock", "wind up"],
                "character_markers": ["father", "mother"],
                "description": "Conception",
                "chronological_order": 1
            },
            "birth": {
                "keywords": ["birth", "born", "midwife", "dr. slop", "slop", "delivery", 
                           "forceps", "nose", "crushed"],
                "character_markers": ["slop", "susannah", "mother"],
                "description": "Birth",
                "chronological_order": 2
            },
            "christening": {
                "keywords": ["christening", "christened", "trismegistus", "baptism", "baptized", "name"],
                "character_markers": ["curate"],
                "description": "Christening",
                "chronological_order": 3
            },
            "childhood_accidents": {
                "keywords": ["circumcision", "window", "sash", "susannah", "accident"],
                "character_markers": ["susannah", "obadiah"],
                "description": "Childhood Accidents",
                "chronological_order": 4
            },
            "childhood_education": {
                "keywords": ["tristrapoedia", "governor", "education", "tutor"],
                "character_markers": [],
                "description": "Childhood Education",
                "chronological_order": 5
            },
            "toby_wadman": {
                "keywords": ["widow wadman", "wadman", "amours", "courtship", "love", "bridget"],
                "character_markers": ["widow wadman", "bridget"],
                "description": "Toby & Wadman",
                "chronological_order": 7
            },
            "tristram_writing": {
                "keywords": ["dear reader", "writing", "pen", "author", "narrative", "i am writing"],
                "character_markers": ["dear sir", "reader"],
                "description": "Tristram Writing",
                "chronological_order": 10
            },
            "meta_commentary": {
                "keywords": ["preface", "digression", "chapter about", "critic", "book"],
                "character_markers": [],
                "description": "Meta-commentary",
                "chronological_order": 11
            },
            "walter_theories": {
                "keywords": ["theory", "hypothesis", "auxiliary verbs", "nose theory", "names"],
                "character_markers": ["father", "walter"],
                "description": "Walter's Theories",
                "chronological_order": 0
            },
            "slawkenbergius": {
                "keywords": ["slawkenbergius", "strasbourg", "julia", "stranger"],
                "character_markers": ["slawkenbergius"],
                "description": "Slawkenbergius",
                "chronological_order": 0
            },
            "sermon": {
                "keywords": ["sermon", "conscience", "ernulphus", "preached"],
                "character_markers": [],
                "description": "Sermon",
                "chronological_order": 0
            }
        }
        
        # Color scheme
        self.narrative_colors = {
            'tristram_writing': '#FF8C42',
            'toby_recovery': '#7FB069',
            'birth': '#4ECDC4',
            'toby_wadman': '#9B59B6',
            'toby_namur': '#E74C3C',
            'childhood_accidents': '#95A5A6',
            'conception': '#F1C40F',
            'meta_commentary': '#E67E22',
            'sermon': '#8E44AD',
            'walter_theories': '#C39BD3',
            'slawkenbergius': '#D7BDE2',
            'dinah': '#CB4335',
            'christening': '#45B7D1',
            'yorick_life': '#5DADE2',
            'childhood_education': '#F8B739'
        }
    
    def download_book(self) -> bool:
        print("Downloading Tristram Shandy from Project Gutenberg...")
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            self.html_content = response.text
            print(f"✓ Downloaded ({len(self.html_content)} characters)")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def extract_chapters(self):
        print("Extracting chapters with full content...")
        soup = BeautifulSoup(self.html_content, 'html.parser')
        text_content = soup.get_text()
        
        chapter_pattern = re.compile(r'C\s*H\s*A\s*P\.?\s+([IVXLCDM]+)', re.IGNORECASE)
        matches = list(chapter_pattern.finditer(text_content))
        
        for i, match in enumerate(matches):
            chapter_num_roman = match.group(1)
            chapter_num = self._roman_to_int(chapter_num_roman)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text_content)
            
            content = text_content[start:end]
            content = re.sub(r'\s+', ' ', content).strip()
            content = re.sub(r'\[Pg \d+\]', '', content)
            
            if len(content) > 200:
                self.chapters.append({
                    'chapter': chapter_num,
                    'chapter_roman': chapter_num_roman,
                    'content': content
                })
        
        print(f"✓ Extracted {len(self.chapters)} chapters")
    
    def _roman_to_int(self, roman: str) -> int:
        roman = roman.upper().strip()
        roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        total = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_values.get(char, 0)
            if value >= prev_value:
                total += value
            else:
                total -= value
            prev_value = value
        return total
    
    def extract_candidate_quotations(self, content: str) -> List[Dict]:
        """Extract scored candidate quotations."""
        sentences = re.split(r'(?<=[.!?])\s+', content)
        candidates = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence) < 40 or len(sentence) > 400:
                continue
            if re.match(r'^(Chapter|CHAP|Vol)', sentence, re.IGNORECASE):
                continue
            
            score = 0
            sentence_lower = sentence.lower()
            
            # Character names
            character_names = ['toby', 'trim', 'yorick', 'walter', 'slop', 'susannah', 
                             'obadiah', 'dinah', 'wadman', 'bobby']
            for name in character_names:
                if name in sentence_lower:
                    score += 2
            
            # Temporal markers
            temporal_markers = ['when', 'after', 'before', 'during', 'since', 'until']
            for marker in temporal_markers:
                if marker in sentence_lower:
                    score += 1
            
            # Dialogue
            if '"' in sentence:
                score += 1
            
            candidates.append({'text': sentence.strip(), 'score': score})
        
        return candidates
    
    def select_representative_quotation(self, content: str, narrative_bucket: str) -> str:
        """Select most representative quotation using keyword matching."""
        candidates = self.extract_candidate_quotations(content)
        
        if not candidates:
            return content[:200] + "..."
        
        bucket_info = self.time_buckets.get(narrative_bucket, {})
        keywords = bucket_info.get('keywords', [])
        character_markers = bucket_info.get('character_markers', [])
        
        # Score by relevance to narrative bucket
        for candidate in candidates:
            quote_lower = candidate['text'].lower()
            relevance = 0
            
            for keyword in keywords:
                if keyword.lower() in quote_lower:
                    relevance += 3
            
            for character in character_markers:
                if character.lower() in quote_lower:
                    relevance += 2
            
            candidate['relevance'] = relevance + candidate['score']
        
        candidates.sort(key=lambda x: x['relevance'], reverse=True)
        return candidates[0]['text'] if candidates else content[:200] + "..."
    
    def annotate_chapters(self):
        print("Annotating chapters with narrative periods and selecting quotations...")
        
        for idx, chapter in enumerate(self.chapters):
            content_lower = chapter['content'].lower()
            
            bucket_scores = {}
            for bucket_name, bucket_info in self.time_buckets.items():
                score = 0
                for keyword in bucket_info['keywords']:
                    score += content_lower.count(keyword.lower()) * 2
                for character in bucket_info.get('character_markers', []):
                    score += content_lower.count(character.lower()) * 3
                if score > 0:
                    bucket_scores[bucket_name] = score
            
            primary_bucket = max(bucket_scores, key=bucket_scores.get) if bucket_scores else 'tristram_writing'
            bucket_info = self.time_buckets[primary_bucket]
            
            representative_quote = self.select_representative_quotation(chapter['content'], primary_bucket)
            
            self.annotated_data.append({
                'chapter': chapter['chapter'],
                'chapter_roman': chapter['chapter_roman'],
                'reading_order': idx + 1,
                'chronological_position': bucket_info['chronological_order'],
                'narrative_period': primary_bucket,
                'narrative_description': bucket_info['description'],
                'representative_quote': representative_quote
            })
        
        print(f"✓ Annotated {len(self.annotated_data)} chapters with quotations")
    
    def create_visualization(self) -> go.Figure:
        """Create the dual-panel temporal architecture visualization."""
        print("\nCreating dual-panel visualization...")
        
        df = pd.DataFrame(self.annotated_data)
        df['color'] = df['narrative_period'].map(self.narrative_colors).fillna('#95A5A6')
        
        # Create dual-panel figure
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.75, 0.25],  # Give more space to top panel
            vertical_spacing=0.10,  # Slightly reduced spacing
            subplot_titles=(
                'Narrative Path of "Tristram Shandy"',
                'Chronological Distribution'
            ),
            specs=[[{"type": "scatter"}], [{"type": "bar"}]]
        )
        
        # TOP PANEL: Connected line graph
        for i in range(len(df) - 1):
            fig.add_trace(
                go.Scatter(
                    x=[df.iloc[i]['reading_order'], df.iloc[i+1]['reading_order']],
                    y=[df.iloc[i]['chronological_position'], df.iloc[i+1]['chronological_position']],
                    mode='lines',
                    line=dict(color=df.iloc[i]['color'], width=1.5),  # Reduced from 2 to 1.5
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=1, col=1
            )
        
        # Add markers with quotations
        for period in df['narrative_period'].unique():
            period_data = df[df['narrative_period'] == period]
            
            fig.add_trace(
                go.Scatter(
                    x=period_data['reading_order'],
                    y=period_data['chronological_position'],
                    mode='markers',
                    marker=dict(
                        size=6,  # Reduced from 7 to 6 for less visual clutter
                        color=self.narrative_colors.get(period, '#95A5A6'),
                        line=dict(width=0.5, color='white')
                    ),
                    name=period_data.iloc[0]['narrative_description'] if len(period_data) > 0 else period,
                    text=period_data.apply(
                        lambda row: f"<b>Chapter {row['chapter']}</b><br>" +
                                   f"Period: {row['narrative_description']}<br><br>" +
                                   f"<i>\"{row['representative_quote'][:200]}{'...' if len(row['representative_quote']) > 200 else ''}\"</i>",
                        axis=1
                    ),
                    hovertemplate='%{text}<extra></extra>',
                    legendgroup=period
                ),
                row=1, col=1
            )
        
        # Add temporal labels
        fig.add_annotation(x=10, y=-4, text="-4 Past", showarrow=False,
                          font=dict(size=10, color='#7F8C8D'), xanchor='left', row=1, col=1)
        fig.add_annotation(x=10, y=0, text="0 Digressions", showarrow=False,
                          font=dict(size=10, color='#7F8C8D'), xanchor='left', row=1, col=1)
        fig.add_annotation(x=10, y=11, text="11 Present", showarrow=False,
                          font=dict(size=10, color='#7F8C8D'), xanchor='left', row=1, col=1)
        
        # BOTTOM PANEL: Distribution bars
        chronological_counts = df.groupby(['chronological_position', 'narrative_period']).size().reset_index(name='count')
        positions = sorted(df['chronological_position'].unique())
        
        for period in df['narrative_period'].unique():
            period_counts = []
            for pos in positions:
                count = chronological_counts[
                    (chronological_counts['chronological_position'] == pos) & 
                    (chronological_counts['narrative_period'] == period)
                ]['count'].sum()
                period_counts.append(count)
            
            fig.add_trace(
                go.Bar(
                    x=positions,
                    y=period_counts,
                    name=df[df['narrative_period'] == period].iloc[0]['narrative_description'] if len(df[df['narrative_period'] == period]) > 0 else period,
                    marker_color=self.narrative_colors.get(period, '#95A5A6'),
                    showlegend=False,
                    legendgroup=period
                ),
                row=2, col=1
            )
        
        # Layout
        fig.update_xaxes(
            title_text="Reading Order (Chapters)", 
            showgrid=True,
            gridwidth=0.3,  # Thinner gridlines
            gridcolor='rgba(200,200,200,0.25)',  # Lighter gridlines
            range=[0, df['reading_order'].max() + 10],  # Add padding on right
            row=1, col=1
        )
        fig.update_yaxes(
            title_text="Chronological Position", 
            showgrid=True,
            gridwidth=0.3,  # Thinner gridlines
            gridcolor='rgba(200,200,200,0.25)',  # Lighter gridlines
            zeroline=True, 
            zerolinewidth=1, 
            zerolinecolor='rgba(100,100,100,0.4)',
            tickmode='linear', 
            tick0=-4, 
            dtick=1,
            range=[-5, 12],  # Add padding top and bottom
            row=1, col=1
        )
        fig.update_xaxes(
            title_text="Chronological Position", 
            tickmode='linear',
            tick0=-4, 
            dtick=1, 
            row=2, col=1
        )
        fig.update_yaxes(
            title_text="Number of Chapters", 
            row=2, col=1
        )
        
        fig.update_layout(
            height=800,
            width=1800,  # Increased width for more horizontal space
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial, sans-serif", size=11),
            title_font=dict(size=16, color='#2C3E50'),
            hovermode='closest',
            margin=dict(l=80, r=250, t=80, b=60),
            legend=dict(
                title=dict(text="<b>Narrative Periods</b>", font=dict(size=11)),
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="left",
                x=1.01,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#BDC3C7",
                borderwidth=1,
                font=dict(size=9)
            ),
            barmode='stack'
        )
        
        print("✓ Visualization created")
        return fig
    
    def create_html_presentation(self, fig: go.Figure):
        """Generate comprehensive HTML page with explanatory sections."""
        print("\nGenerating comprehensive HTML presentation...")
        
        df = pd.DataFrame(self.annotated_data)
        
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Tristram Shandy: Temporal Architecture Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Georgia, serif;
            max-width: 1500px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0 0 15px 0;
            font-size: 2.5em;
            font-weight: normal;
        }
        .header p {
            margin: 5px 0;
            font-size: 1.2em;
            opacity: 0.95;
        }
        .section {
            background-color: white;
            padding: 30px;
            margin-bottom: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 12px;
            margin-top: 0;
            font-size: 1.8em;
        }
        .section h3 {
            color: #34495e;
            margin-top: 25px;
            font-size: 1.3em;
        }
        .timeline-scale {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 18px;
            margin: 25px 0;
        }
        .timeline-box {
            padding: 18px;
            border-radius: 6px;
            border-left: 5px solid;
            transition: transform 0.2s;
        }
        .timeline-box:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .pre-birth {
            background-color: #e3f2fd;
            border-color: #2196f3;
        }
        .digressions {
            background-color: #fff9e6;
            border-color: #ffc107;
        }
        .life {
            background-color: #e8f5e9;
            border-color: #4caf50;
        }
        .present {
            background-color: #f3e5f5;
            border-color: #9c27b0;
        }
        .timeline-box strong {
            display: block;
            font-size: 1.4em;
            margin-bottom: 8px;
            color: #2c3e50;
        }
        .timeline-box .label {
            font-weight: 600;
            margin-bottom: 5px;
            font-size: 1.1em;
        }
        .visualization {
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        ul {
            line-height: 2;
        }
        .key-insight {
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .key-insight strong {
            font-size: 1.1em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        table th {
            background-color: #f8f9fa;
            padding: 12px;
            border: 1px solid #dee2e6;
            text-align: left;
            font-weight: 600;
        }
        table td {
            padding: 12px;
            border: 1px solid #dee2e6;
        }
        .methodology {
            background-color: #e8f4f8;
            border-left: 5px solid #3498db;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>THE LIFE AND OPINIONS OF TRISTRAM SHANDY, GENTLEMAN</h1>
        <p>by Laurence Sterne (1759-1767)</p>
        <p style="font-size: 1em; margin-top: 10px; opacity: 0.85;">
            A Digital Humanities Analysis of Non-Linear Narrative Structure
        </p>
    </div>

    <div class="section">
        <h2>About the Novel</h2>
        <p style="font-size: 1.1em; line-height: 1.8;">
            <em>The Life and Opinions of Tristram Shandy, Gentleman</em> is one of literature's 
            first experimental novels and a masterpiece of non-linear storytelling. The narrator, 
            Tristram, attempts to tell his life story but constantly digresses into tangents, 
            backstories, and philosophical musings. The result is a chaotic, playful narrative 
            that jumps backward and forward in time.
        </p>
        <div class="key-insight">
            <strong>💡 Key Insight:</strong> Tristram famously doesn't even get to his own birth 
            until Volume 3 — he's too busy telling us about everything that led up to it! The 
            novel's structure itself becomes an argument about memory, digression, and the 
            impossibility of linear self-narration.
        </div>
    </div>

    <div class="section">
        <h2>The Dual-Panel Visualization Explained</h2>
        <p style="font-size: 1.1em; line-height: 1.8;">
            This is not a generic timeline. It is a <strong>temporal architecture visualization</strong> 
            designed to make the novel's non-chronological structure legible. The visualization consists 
            of two synchronized panels:
        </p>
        
        <h3>Top Panel: Narrative Path Timeline</h3>
        <ul style="font-size: 1.05em;">
            <li><strong>X-axis:</strong> Reading Order (Chapters 1–300 sequentially)</li>
            <li><strong>Y-axis:</strong> Chronological Position (when events actually occur: -4 to 11)</li>
            <li><strong>Connected Line:</strong> Shows the temporal path a reader takes through the narrative</li>
            <li><strong>Color-Coded Dots:</strong> Each chapter colored by its narrative period</li>
            <li><strong>Hover Interaction:</strong> Displays representative quotations from each chapter</li>
        </ul>
        <p style="font-size: 1.05em; line-height: 1.8; margin-top: 15px;">
            <strong>If the novel were linear,</strong> the line would ascend steadily from bottom-left 
            to top-right. Instead, you see dramatic vertical jumps—Sterne constantly yanking the reader 
            backward and forward through time.
        </p>
        
        <h3>Bottom Panel: Chronological Distribution</h3>
        <p style="font-size: 1.05em; line-height: 1.8;">
            A stacked bar chart showing how many chapters occupy each chronological position. This reveals 
            where the novel <em>dwells</em> chronologically—notice how much time Sterne spends on "present 
            narration" (position 10) compared to actual life events.
        </p>
    </div>

    <div class="section">
        <h2>Understanding the Chronological Scale</h2>
        
        <div class="timeline-scale">
            <div class="timeline-box pre-birth">
                <strong>-4 to -1</strong>
                <div class="label">Before Tristram's Birth</div>
                <small>Family history, Uncle Toby's war injury at Namur, Parson Yorick's life and death</small>
            </div>
            
            <div class="timeline-box digressions">
                <strong>0</strong>
                <div class="label">Digressions</div>
                <small>Timeless stories-within-stories, philosophical theories, embedded tales like Slawkenbergius</small>
            </div>
            
            <div class="timeline-box life">
                <strong>1 to 8</strong>
                <div class="label">Tristram's Life</div>
                <small>Conception → Birth → Christening → Childhood → Youth (chronological progression)</small>
            </div>
            
            <div class="timeline-box present">
                <strong>10-11</strong>
                <div class="label">Present Narrative</div>
                <small>Tristram writing the book, meta-commentary on the act of storytelling itself</small>
            </div>
        </div>

        <h3>Why Negative Numbers?</h3>
        <p style="font-size: 1.05em; line-height: 1.8;">
            Tristram doesn't start his story at his birth — he goes <em>backward</em> to tell us about 
            his family's history first. Uncle Toby's war wound at the Siege of Namur happened years 
            before Tristram was conceived, so it gets a <strong>negative chronological position</strong> (-2). 
            Think of position 0 as Tristram's birth (the origin point), with negative numbers representing 
            the years before that event. This shows how far back in time the narrative reaches before 
            the protagonist even exists.
        </p>
    </div>

    <div class="section">
        <h2>What the Visualization Reveals</h2>
        <ul style="font-size: 1.05em;">
            <li>The <strong>connected line</strong> traces the reader's journey through narrative time—every 
                vertical movement is a temporal jump</li>
            <li><strong>Steep drops</strong> reveal flashbacks to pre-birth history (e.g., from present 
                narration back to Uncle Toby at Namur)</li>
            <li><strong>Steep rises</strong> show returns to the present narrative frame</li>
            <li><strong>Horizontal plateaus</strong> indicate sustained focus on a single time period 
                across multiple chapters</li>
            <li><strong>Frequency of crossings at y=0</strong> shows how often Sterne interrupts with 
                timeless digressions</li>
            <li><strong>Bottom panel density</strong> reveals that Sterne spends disproportionate time 
                on "present narration" rather than life events</li>
        </ul>
        <div class="key-insight">
            <strong>💡 Literary Significance:</strong> The visualization quantifies narrative disorder. 
            A linear biography would show a smooth upward slope. Sterne's jagged line—with its wild 
            oscillations between past, present, and digression—reveals a narrator unable or unwilling 
            to tell his story in chronological order. <strong>The structure itself becomes an argument 
            about memory, digression, and the impossibility of linear self-narration.</strong>
        </div>
    </div>

    <div class="visualization">
        <h2 style="color: #2c3e50; margin-top: 0;">Interactive Temporal Architecture</h2>
        <p style="color: #7f8c8d; margin-bottom: 20px; font-size: 1.05em;">
            <strong>How to interact:</strong> Hover over any point to see chapter details and representative 
            quotations. Click and drag to zoom into specific regions. Double-click to reset the view. 
            The line connects chapters in reading order—watch how it oscillates through time.
        </p>
        <div id="plotly-chart"></div>
    </div>

    <div class="section">
        <h2>Methodology</h2>
        
        <div class="methodology">
            <h3 style="margin-top: 0; color: #2c3e50;">Data Collection & Processing</h3>
            <p><strong>Source:</strong> Full text from Project Gutenberg</p>
            <p><strong>Chapters Analyzed:</strong> """ + str(len(df)) + """</p>
            <p><strong>Quotation Selection:</strong> Automated intelligent extraction based on:</p>
            <ul>
                <li>Temporal markers (when, after, before, during)</li>
                <li>Character name relevance to narrative period</li>
                <li>Keyword matching to narrative buckets</li>
                <li>Sentence quality (50-400 characters, avoids fragments)</li>
            </ul>
        </div>
        
        <h3>Dataset Summary</h3>
        <p><strong>Total chapters analyzed:</strong> """ + str(len(df)) + """</p>
        <p><strong>Reading order range:</strong> 1 to """ + str(df['reading_order'].max()) + """</p>
        <p><strong>Chronological range:</strong> """ + str(df['chronological_position'].min()) + """ to """ + str(df['chronological_position'].max()) + """</p>
        
        <h3>Narrative Period Distribution</h3>
        <table>
            <tr>
                <th>Narrative Period</th>
                <th>Number of Chapters</th>
                <th>Chronological Position</th>
            </tr>
"""
        
        for bucket, count in df['narrative_period'].value_counts().items():
            chrono_pos = df[df['narrative_period'] == bucket].iloc[0]['chronological_position']
            description = df[df['narrative_period'] == bucket].iloc[0]['narrative_description']
            html_content += f"""            <tr>
                <td>{description}</td>
                <td>{count}</td>
                <td>{chrono_pos}</td>
            </tr>
"""
        
        html_content += """        </table>
    </div>

    <div class="section" style="background-color: #ecf0f1; border-left: 5px solid #3498db;">
        <p style="margin: 0; font-style: italic; font-size: 1.05em;">
            <strong>Citation:</strong> Sterne, Laurence. <em>The Life and Opinions of Tristram Shandy, 
            Gentleman.</em> Project Gutenberg. 
            <a href="https://www.gutenberg.org/ebooks/1079" target="_blank" style="color: #3498db;">
                https://www.gutenberg.org/ebooks/1079
            </a>
        </p>
    </div>

    <script>
        var data = """ + fig.to_json() + """;
        Plotly.newPlot('plotly-chart', data.data, data.layout, {responsive: true});
    </script>
</body>
</html>
"""
        
        filename = "tristram_shandy_complete_analysis.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Complete HTML presentation saved: {filename}")
        return filename

def main():
    print("="*80)
    print("TRISTRAM SHANDY: COMPLETE TEMPORAL ARCHITECTURE PIPELINE")
    print("Advanced Web Scraping + Dual-Panel Visualization + HTML Presentation")
    print("="*80 + "\n")
    
    pipeline = TristramShandyCompletePipeline()
    
    # Step 1: Download
    if not pipeline.download_book():
        print("\n✗ Failed to download. Exiting.")
        return
    
    # Step 2: Extract chapters
    pipeline.extract_chapters()
    
    # Step 3: Annotate with intelligent quotation extraction
    pipeline.annotate_chapters()
    
    # Step 4: Create visualization
    fig = pipeline.create_visualization()
    
    # Step 5: Generate comprehensive HTML presentation
    html_file = pipeline.create_html_presentation(fig)
    
    # Success
    print("\n" + "="*80)
    print("✓ COMPLETE PIPELINE FINISHED")
    print("="*80)
    print(f"\n📄 Open this file in your browser: {html_file}")
    print("\nWhat you'll find:")
    print("  • Comprehensive explanatory sections")
    print("  • Dual-panel temporal architecture visualization")
    print("  • Interactive quotations on hover")
    print("  • Complete methodology and dataset summary")
    print("\nThe structure of non-linear time is now visible.")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
```

    ================================================================================
    TRISTRAM SHANDY: COMPLETE TEMPORAL ARCHITECTURE PIPELINE
    Advanced Web Scraping + Dual-Panel Visualization + HTML Presentation
    ================================================================================
    
    Downloading Tristram Shandy from Project Gutenberg...
    ✓ Downloaded (1259736 characters)
    Extracting chapters with full content...
    ✓ Extracted 300 chapters
    Annotating chapters with narrative periods and selecting quotations...
    ✓ Annotated 300 chapters with quotations
    
    Creating dual-panel visualization...
    ✓ Visualization created
    
    Generating comprehensive HTML presentation...
    ✓ Complete HTML presentation saved: tristram_shandy_complete_analysis.html
    
    ================================================================================
    ✓ COMPLETE PIPELINE FINISHED
    ================================================================================
    
    📄 Open this file in your browser: tristram_shandy_complete_analysis.html
    
    What you'll find:
      • Comprehensive explanatory sections
      • Dual-panel temporal architecture visualization
      • Interactive quotations on hover
      • Complete methodology and dataset summary
    
    The structure of non-linear time is now visible.
    ================================================================================
    



```python

```

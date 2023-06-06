-- schema for a basketball database

create database league;

create table conference (
    id int primary key,
    name varchar(50) not null,
    abbv varchar(3) not null
);

create table position (
    id int primary key,
    name varchar(50) not null,
    abbv char(2) not null
);

create table player (
    id int primary key,
    name varchar(50) not null,
    dob date not null,
    hgt int not null,
    wgt int not null,
    pos int not null,
    injured boolean default false,
    teamId int,
    foreign key (position) references position(id),
    foreign key (teamId) references team (id)
);

-- create table for player stats and ratings
-- lets say there are 20 players per team
-- 30 teams in the league
-- total players in the league ~ 600
-- one season - each player plays 82 games
-- total playerStat entries in one season ~ 49200 (50k)
-- after 20 seasons, total playerStat entries ~ 984000 (1M)
create table playerStat (
    pId int not null,
    gId int not null,
    sId int not null,
    ast int default 0,
    asta int default 0,
    benchTime int default 0,
    blk int default 0,
    courtTime int default 0,
    drb int default 0,
    energy int default 100,
    fg int default 0,
    fgInside int default 0,
    fgMidrange int default 0,
    fgThreepoint int default 0,
    fga int default 0,
    fgaInside int default 0,
    fgaMidrange int default 0,
    fgaThreepoint int default 0,
    ft int default 0,
    fta int default 0,
    g int default 0,
    gs int default 0,
    sp int default 0,
    orb int default 0,
    pf int default 0,
    pts int default 0,
    stl int default 0,
    tov int default 0,
    primary key (pId, gId, sId),
    foreign key (pId) references player (id),
    foreign key (gId) references game (id)
);

create table playerRating (
    pId int not null,
    sId int not null,
    hgt int default 0,
    stre int default 0,
    stam int default 0,
    spd int default 0,
    jmp int default 0,
    ins int default 0,
    mid int default 0,
    tp int default 0,
    ft int default 0,
    pss int default 0,
    hndl int default 0,
    reb int default 0,
    oiq int default 0,
    diq int default 0,
    dur int default 0,
    primary key (pId, sId),
    foreign key (pId) references player (id)
);

-- create team table
create table team (
    id int primary key,
    name varchar(50) not null,
    abbv varchar(3) not null,
    conf int,
    -- arena varchar(50),
    cap int not null,
    -- city varchar(50),
    -- state varchar(50),
    w int not null default 0,
    l int not null default 0,
    foreign key (conference) references conference (id)
);

-- create table for team season stats
create table teamStats (
    tId int,
    sId int,
    conf int not null,
    w int not null default 0,
    l int not null default 0,
    wConf int not null default 0,
    lConf int not null default 0,
    primary key (tId, sId),
    foreign key (tId) references team (id),
    foreign key (sId) references season (id),
    foreign key (conf) references conference (id)
);

-- create game table
create table game (
    id int,
    sId int,
    tIdHome int not null,
    tIdAway int not null,
    constraint teamIdCheck check (tIdHome != tIdAway),
    date date not null,
    homeScore int not null default 0,
    awayScore int not null default 0,
    leadChanges int not null default 0,
    largestLead int not null default 0,
    primary key (id, sId),
    foreign key (sId) references season (id),
    foreign key (tIdHome) references team (id),
    foreign key (tIdAway) references team (id)
);

-- create table for game players
-- each season = 1230 games
-- each game <= 20 players
-- total gamePlayer entries in one season ~ 24600
-- after 20 seasons, total gamePlayer entries ~ 492000 (500k)
create table gamePlayer (
    pId int not null,
    tId int not null,
    gId int not null,
    sId int not null,
    primary key (sId, gId, pId),
    foreign key (sId) references season (id),
    foreign key (gId) references game (id),
    foreign key (pId) references player (id),
    foreign key (tId) references team (id)
);

-- create table for game stats
-- no
-- create table for game ratings
-- no

-- I would like to save the events of the game, so that I can always replay it
-- Define a class to represent an event in the game, with attributes such as the time the event occurred, the type of event (e.g., shot made, foul, turnover, etc.), and any relevant details about the event (e.g., the player who made the shot).
-- Create an instance of this class each time an event occurs during the game, and add it to a list of events.
-- When the game is over, save the list of events to a file.
-- When the user wants to replay a game, read the list of events from the file, and replay the game by playing back the events in the list.
-- create table for game events
-- each season = 1230 games
-- one team <= 300 events per game
-- each game ~ 600 events
-- total gameEvent entries in one season ~ 738000 (750k)
-- after 20 seasons, total gameEvent entries ~ 14760000 (15M)
create table gameEvent (
    
    gId int not null,
    sId int not null,
    qtr int not null,
    time int not null,
    type char(3) not null,    -- JUM, 3P(A), FG(A), FT(A), REB, STL/TOV, BLK, FOUL, SUB
    tIdOff int not null,    -- team on offense
    tIdDef int not null,    -- team on defense
    constraint teamIdCheck check (tIdOff != tIdDef),
    pIdOff int,
    pAstId int,
    constraint playerIdCheck check (pIdOff != pAstId),
    pIdDef int,
    subsIn varchar(50),
    subsOut varchar(50),
    primary key (gId, sId, qtr, time, type),
    foreign key (gId) references game (id),
    foreign key (sId) references season (id),
    foreign key (tIdOff) references team (id),
    foreign key (tIdDef) references team (id),
    foreign key (pIdOff) references player (id),
    foreign key (pAstId) references player (id),
    foreign key (pIdDef) references player (id)
);